from pytesmo.validation_framework.metric_calculators_adapters import TsDistributor
from pytesmo.time_series.grouping import YearlessDatetime
from typing import Optional, List, Tuple, Dict
import yaml
import os
from datetime import datetime


class IntraAnnualSlicesDefault:
    '''
    Class to load intra annual slice definitions from a YAML file.
    Such a file should contain a dictionaries with the following structure:

    seasons:
        S1: [[12, 1], [2, 28]]      # December 1st to February 28th
        S2: [[3, 1], [5, 31]]       # March 1st to May 31st
        S3: [[6, 1], [8, 31]]       # June 1st to August 31st
        S4: [[9, 1], [11, 30]]      # September 1st to November 30th

    These dictionaries will be loaded as properties of the class, so that they can be accessed later on and be treated as the default.

    Parameters
    ----------

    default_file : str, optional
        Path to the YAML file containing the intra annual slice definitions, by default None

    '''

    def __init__(self, default_file: Optional[str] = None) -> None:
        if not default_file:
            default_file = os.path.abspath(
                'intra_annual_slices_definition.yml'
            )  # if no file is provided, use the default one

        if not os.path.isfile(default_file):
            raise FileNotFoundError(
                f'File {default_file} not found. Please provide a valid path to a YAML file, containing the intra annual slice definitions.'
            )
        else:
            self.__default_file = default_file

        # Load YAML data upon initialization
        self.yaml_data = self.__load_yaml_data()
        self.available_defaults = list(self.yaml_data.keys())

    def __load_yaml_data(self) -> dict:
        '''Reads and loads the YAML file into a dictionary.

        Parameters
        ----------
        None

        Returns
        -------
        dict
            Dictionary containing the default intra annual slice definitions.
        '''

        with open(self.__default_file, 'r') as f:
            return yaml.safe_load(f)


class IntraAnnualSlicer(IntraAnnualSlicesDefault):
    '''Class to create custom intra annual slices, based on the default definitions.

    Parameters
    ----------
    intra_annual_slice_type : str
        Type of intra annual slice to be created. Must be one of the available default types. Officially, "months" and "seasons" are implemented. The user can implement their own defaults, though (see `IntraAnnualSlicesDefault`). Default is "months".
    overlap : int, optional
        Number of days to be added/subtracted to the beginning/end of the intra annual slice. Default is 0.
    default_file : str, optional
        Path to the YAML file containing the intra annual slice definitions, by default None (meaning the default file will be used)
    '''

    def __init__(self,
                 intra_annual_slice_type: Optional[str] = 'months',
                 overlap: Optional[int] = 0,
                 default_file: Optional[str] = None):
        self.overlap = overlap
        self.intra_annual_slice_type = intra_annual_slice_type
        super().__init__(default_file=default_file)

        if self.intra_annual_slice_type not in self.available_defaults:
            raise ValueError(
                f'Invalid intra annual slice type. Available types are: {self.available_defaults}'
            )

    def __date_to_doy(self, date_tuple: Tuple[int, int]) -> int:
        '''Converts a date list [month, day] to a day of the year (doy). Leap years are neglected.

        Parameters
        ----------
        date_tuple : List[int]
            List containing the month and day of the date to be converted. The year is not required, as it is not used in the conversion.

        Returns
        -------
        int
            Day of the year (doy) corresponding to the date provided.
        '''

        _doy = YearlessDatetime(date_tuple[0], date_tuple[1]).doy
        if _doy > 60:  # assume NO leap year
            _doy -= 1

        return _doy

    def __doy_to_date(self, doy: int) -> Tuple[int, int]:
        '''Converts a day of the year (doy) to a date tuple (month, day). Leap years are neglected.

        Parameters
        ----------
        doy : int
            Day of the year (doy) to be converted.

        Returns
        -------
        Tuple[int]
            Tuple containing the month and day corresponding to the doy provided.
        '''

        date = datetime.strptime(str(doy), '%j')
        month = date.strftime('%m')
        day = date.strftime('%d')

        return int(month), int(day)

    def __update_date(self, date: Tuple[int, int],
                      overlap_direction: float) -> Tuple[int, int]:
        '''Updates a date tuple (month, day) by adding/subtracting the overlap value to/from it.

        Parameters
        ----------
        date : Tuple[int]
            Date to be updated.
        overlap_direction : float
            Direction of the overlap. Must be either -1 or +1. -1: subtract overlap value from date; +1: add overlap value to date.

        Returns
        -------
        Tuple[int]
            Updated date tuple.
        '''

        overlap_direction = overlap_direction / abs(
            overlap_direction)  # making sure it's either -1 or +1
        _doy = self.__date_to_doy(date)
        _doy += int(overlap_direction * self.overlap)

        if _doy < 1:
            _doy = 365 - abs(_doy)
        elif _doy > 365:
            _doy = _doy - 365

        return self.__doy_to_date(_doy)

    def _custom_intra_annual_slice(self):
        return {
            key: (self.__update_date(val[0], overlap_direction=-1),
                  self.__update_date(val[1], overlap_direction=+1))
            for key, val in self.yaml_data[
                self.intra_annual_slice_type].items()
        }

    @property
    def custom_intra_annual_slices(self) -> Dict[str, TsDistributor]:
        '''Custom intra annual slice based, on the default definitions and the overlap value.

        Parameters
        ----------
        None

        Returns
        -------
        dict[str, TsDistributor]
            Dictionary containing the custom intra annual slice definitions.
        '''

        def tsdistributer(_begin_date: Tuple[int],
                          _end_date: Tuple[int]) -> TsDistributor:
            return TsDistributor(yearless_date_ranges=[(YearlessDatetime(
                *_begin_date), YearlessDatetime(*_end_date))])

        return {
            key: tsdistributer(val[0], val[1])
            for key, val in self._custom_intra_annual_slice().items()
        }

    @property
    def names(self) -> List[str]:
        '''Returns the names of the intra annual slices.

        Parameters
        ----------
        None

        Returns
        -------
        List[str]
            List containing the names of the intra annual slices.
        '''

        return list(self._custom_intra_annual_slice().keys())

    @property
    def metadata(self) -> dict:
        '''Returns the metadata of the intra annual slices.

        Parameters
        ----------
        None

        Returns
        -------
        Dict[str, Union[str, List[str]]]
            Dictionary containing the metadata of the intra annual slices.
        '''

        def _date_formatter(_date: Tuple[int, int]) -> str:
            return f'{_date[0]:02d}-{_date[1]:02d}'

        return {
            'Intra annual slice type':
            self.intra_annual_slice_type,
            'Overlap':
            f'{self.overlap} days',
            'Names_Dates [MM-DD]':
            '(MM-DD):' + (', ').join([
                f'{key}: {_date_formatter(val[0])} to {_date_formatter(val[1])}'
                for key, val in self._custom_intra_annual_slice().items()
            ])
        }
