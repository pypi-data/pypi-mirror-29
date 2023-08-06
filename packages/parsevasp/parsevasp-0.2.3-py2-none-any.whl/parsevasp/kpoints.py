#!/usr/bin/python
import sys
import logging
import numpy as np
from collections import Counter
import StringIO

import utils


class Kpoints(object):

    def __init__(self, kpoints_string=None, kpoints_dict=None,
                 file_path=None, logger=None):
        """Initialize a KPOINTS object and set content as a dictionary.

        Parameters
        ----------
        kpoints_string : string
            A string containing KPOINTS entries. Must contain line
            breaks if multiline, otherwise the KPOINTS will be mangled.
        kpoints_dict : dict
            A dictionary containing the KPOINTS entries.
        file_path : string
            The file path in which the KPOINTS is read.
        logger : object, optional
            A standard Python logger object.


        """

        self.file_path = file_path
        self.kpoints_dict = kpoints_dict
        self.kpoints_string = kpoints_string

        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger

        # check that only one argument is supplied
        if (kpoints_string is not None and kpoints_dict is not None) \
           or (kpoints_string is not None and file_path is not None) \
           or (kpoints_dict is not None and file_path is not None):
            self.logger.error("Please only supply one argument when "
                              "initializing Kpoints. Exiting.")
            sys.exit(1)
        # check that at least one is suplpied
        if (kpoints_string is None and kpoints_dict is None
                and file_path is None):
            self.logger.error("Please supply one argument when "
                              "initializing Kpoints. Exiting.")
            sys.exit(1)

        if file_path is not None:
            # create dictionary from a file
            kpoints_dict = self._from_file()

        if kpoints_string is not None:
            # create dictionary from a string
            kpoints_dict = self._from_string()

        # store entries
        self.entries = kpoints_dict

        # validate dictionary
        self._validate()


    def _from_file(self):
        """Create rudimentary dictionary of entries from a
        file.

        """

        kpoints = utils.readlines_from_file(self.file_path)
        kpoints_dict = self._from_list(kpoints)
        return kpoints_dict

    def _from_string(self):
        """Create rudimentary dictionary of entries from a
        string.

        """

        kpoints = self.kpoints_string.splitlines()
        kpoints_dict = self._from_list(kpoints)
        return kpoints_dict

    def _from_list(self, kpoints):
        """Go through the list and analyze for = and ; in order to
        deentangle grouped entries etc.

        Parameters
        ----------
        kpoints : list
            A list of strings containing each line in the KPOINTS file.

        Returns
        -------
        kpoints_dict : dictionary
            A dictionary containing each KPOINTS tag as a key with the
            associated element.

        Notes
        -----
        No checking for consistency is done here. We do this at a later step
        in order to be able to keep the input methods as clean as posible.

        """

        comment = kpoints[0]
        num_kpoints = int(kpoints[1].split()[0])
        divisions = None
        shifts = None
        tetra = None
        tetra_vol = None
        points = None
        automatic = False
        line_mode = False
        centering = None
        direct = False
        if num_kpoints <= 0:
            # check if we are using automatic mode
            automatic = True
        third_line = kpoints[2].strip()
        if third_line[0].lower() == 'l':
            # line mode is detected
            line_mode = True
        if not automatic and not line_mode:
            direct = False
            if third_line[0].lower() == 'd':
                direct = True
            if not direct:
                self.logger.error("Please supply the KPOINTS in direct "
                                  "coordinates. Exiting.")
                sys.exit(1)
            loopmax = 3
            points = []
            for k in range(num_kpoints):
                kentry = kpoints[k + loopmax].split()
                point = np.zeros(3)
                point[0] = float(kentry[0])
                point[1] = float(kentry[1])
                point[2] = float(kentry[2])
                weight = None
                if len(kentry) > 3:
                    weight = float(kentry[3])
                points.append(Kpoint(point, weight, direct = direct))
            loopmax = num_kpoints + loopmax
            tetra = []
            if len(kpoints) > loopmax:
                if kpoints[loopmax].strip()[0].lower() == "t":
                    # tetrahedron info present
                    loopmax = loopmax + 1
                    if len(kpoints) > loopmax:
                        first_line = kpoints[loopmax].split()
                        num_tetra = int(first_line[0])
                        tetra_vol = float(first_line[1])
                        loopmax = loopmax + 1
                        for tet in range(num_tetra):
                            con_line = kpoints[tet + loopmax].split()
                            if not len(con_line) == 5:
                                self.logger.error("Make sure the connection "
                                                  "line for the tetrahedra info "
                                                  "in the KPOINTS file contains "
                                                  "5 entries. Exiting.")
                                sys.exit(1)
                            tetra.append([int(value) for value in con_line])
        if automatic:
            third_line_char = third_line[0].lower()
            if third_line_char == 'a':
                self.logger.error("We do not support fully automatic inputs. "
                                  "Please instead modify your KPOINTS file "
                                  "in order to explicitely specify Gamma or "
                                  "Monkhorst mode, and the number of samples "
                                  "along each reciprocal lattice "
                                  "vector. Exiting.")
                sys.exit(1)
            elif third_line_char == 'g' or third_line_char == 'm':
                if third_line_char == 'g':
                    centering = "Gamma"
                else:
                    centering = "Monkhorst-Pack"
                divisions = [int(element) for element in kpoints[3].split()]
                if len(kpoints) == 5:
                    shifts = [float(element) for element in kpoints[4].split()]
            elif third_line_char == 'd' or third_line_char == 'c':
                self.logger.error("Expert mode is currently not supported. "
                                  "Exiting.")
                sys.exit(1)
        if line_mode:
            direct = False
            points = []
            if kpoints[3].split()[0][0].lower() == 'r':
                direct = True
            if not direct:
                self.logger.error("Please supply the KPOINTS in direct "
                                  "coordinates. Exiting.")
                sys.exit(1)
            for index in range((len(kpoints)-4)):
                true_index = index + 4
                if kpoints[true_index] != "\n":
                    entry = kpoints[true_index].split()[0:3]
                    coordinate = np.asarray([float(element) for element in entry])
                    point = Kpoint(coordinate, 1.0)
                    points.append(point)
                
        mode = "explicit"
        if automatic:
            mode = "automatic"
        if line_mode:
            mode = "line"
        # add to dictionary
        kpoints_dict = {}
        kpoints_dict["comment"] = comment
        kpoints_dict["divisions"] = divisions
        kpoints_dict["shifts"] = shifts
        kpoints_dict["points"] = points
        kpoints_dict["tetra"] = tetra
        kpoints_dict["tetra_volume"] = tetra_vol
        kpoints_dict["mode"] = mode
        kpoints_dict["centering"] = centering
        kpoints_dict["num_kpoints"] = num_kpoints

        return kpoints_dict

    def modify(self, entry, value, point_number=None):
        """Modify an entry tag in the Kpoints dictionary.

        Parameters
        ----------
        tag : string
            The entry tag of the KPOINTS entry.
        value
            The entry value of the KPOINTS entry.
            Can be either a string for the comment,
            an ndarray for the unitcell or a Kpoint object
            for a point.
        point_number : int, optional
            The point to be modified. If not supplied
            the value have to be a list of Kpoint objects.

        """

        # check allowed entries
        self._check_allowed_entries(entry)
        # check that entries exists
        self._check_dict()
        if point_number is not None:
            # check that a Kpoint() object is supplied
            self._check_point(value)
            # check site number
            self._check_point_number(point_number)
            # check that position is an integer
            if not isinstance(point_number, int):
                self.logger.error("The supplied 'point_number' is "
                                  "not a number (i.e. the index) "
                                  "starting from 1 for the point "
                                  "to be modified. Exiting.")
                sys.exit(1)
            self.entries["points"][point_number] = value
        else:
            if entry == "points":
                self._check_points(points = value)
                # check that all points are in direct, if not,
                # convert
                for point in value:
                    if not point.get_direct():
                        point = self._to_direct(point)
                        self.logger.error("Conversion from reciprocal to "
                                          "direct for the KPOINTS is not yet "
                                          "implemented. Exiting.")
                        sys.exit(1)
            if entry == "comment":
                self._check_comment(comment = value)
            if entry == "divisions":
                self._check_divisions(divisions = value)
            if entry == "shifts":
                self._check_shifts(shifts = value)
            if entry == "tetra":
                self._check_tetra(tetra = value)
            if entry == "tetra_volume":
                self._check_tetra_volume(tetra_volume = value)
            if entry == "centering":
                self._check_centering(centering = value)
            if entry == "mode":
                self._check_mode(mode = value)
            if entry == "num_kpoints":
                self._check_num_kpoints(num_kpoints = value)
                
            self.entries[entry] = value

    def delete_point(self, point_number):
        """Delete the point with the supplied
        number.

        Parameters
        ----------
        point_number : int
            The point number to be deleted, starting
            from 0.

        """

        self._check_points()
        self._check_point_number(point_number)
        del self.entries["points"][point_number]

    def add_point(self, point_number):
        """Add a point with the supplied
        number. If not supplied, add at the end
        of the last element of the specie group

        Parameters
        ----------
        point_number : int
            The point number to be deleted, starting
            from 0.

        """

        # EFL: ADD LATER

    def _check_dict(self):
        """Check that entries is present.

        """

        try:
            entries = self.entries
        except AttributeError:
            self.logger.error("There is no 'entries'. Exiting.")
            sys.exit(1)

        # check that at least divisions or points are set
        # to something else than None
        if (self.entries["divisions"] is None) \
           and (self.entries["points"] is None):
            self.logger.error("You have to set either 'divisions' "
                              "(automatic mode) or the explicit 'points'.")
            sys.exit(1)

    def _check_allowed_entries(self, entry):
        """Check the allowed values of entry.

        Parameters
        ----------
        entry : string
            Contains the entry to be checked.
        
        """

        if not (("comment" in entry) or ("points" in entry) or
                ("tetra" in entry) or ("tetra_volume" in entry) or
                ("divisions" in entry) or ("mode" in entry) or
                ("num_kpoints" in entry) or ("shifts" in entry) or
                ("centering") in entry):
            self.logger.error("Only 'comment', 'points', "
                              "'tetra', 'tetra_volume', 'divisions', "
                              "'shifts', 'mode', 'num_kpoints' or "
                              "'centering' is allowed as input for "
                              "entry. Exiting.")
            sys.exit(1)

    def _check_comment(self, comment = None):
        """Check that the comment entry is present and
        is a string.
        
        Parameters
        ----------
        comment, optional
            The comment to be checked. If not supplied the
            'comment' key in the 'entries' is checked.

        """
        if comment is None:
            try:
                comment = self.entries["comment"]
            except KeyError:
                self.logger.error("There is no key 'comment' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        # allow None for comment
        if self.entries["comment"] is not None:
            if not isinstance(comment, str):
                self.logger.error("The 'comment' is not a string. Exiting.")
                sys.exit(1)

    def _check_points(self, points = None):
        """Check that the points entries are present.

        Parameters
        ----------
        points, optional
            The points to be checked. If not supplied the
            'points' key in the 'entries' is checked.

        """
        
        if points is None:
            try:
                points = self.entries["points"]
            except KeyError:
                self.logger.error("There is no key 'points' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if points is not None:
            # allow points to be none (if no explicit entries are given)
            if not isinstance(points, list):
                self.logger.error("The 'points' entry "
                                  "have to be a list. Exiting.")
                sys.exit(1)
        
    def _check_point(self, point = None):
        """Check that the point entry is a Kpoint() object.

        Parameters
        ----------
        point, optional
            The point to be checked. If not supplied the entries under
            the 'points' key in the 'entries' is checked.

        """
        if point is None:
            try:
                points = self.entries["points"]
            except KeyError:
                self.logger.error("There is no key 'points' in "
                                  "'entries'. Exiting.")
                sys.exit(1)

            for point in points:
                if not isinstance(point, Kpoint):
                    self.logger.error("At least one of the values in 'points' "
                                      "is not a Kpoint() object. Exiting.")
                    sys.exit(1)
        else:
            if not isinstance(point, Kpoint):
                self.logger.error("The 'point' "
                                  "is not a Kpoint() object. Exiting.")
                sys.exit(1)
                
    def _check_point_number(self, point_number):
        """Check that the point_number is an int and that
        it is not out of bounds.

        Parameters
        ----------
        point_number : int
            The point_number to be checked

        """
        
        if not isinstance(point_number, int):
            self.logger.error("The supplied 'point_number' is "
                              "not an integer. Exiting.")
            sys.exit(1)
        points = self.entries["points"]
        if point_number > (len(points)-1):
            self.logger.error("The supplied point_number is larger "
                              "than the number of points. Exiting.")
            sys.exit(1)

    def _check_shifts(self, shifts = None):
        """Check that the shifts are either None or
        a list of three floats.
        
        Parameters
        ----------
        shifts : list, optional
            The shifts to be checked. If not supplied, the
            shifts for the current instance is checked.

        """

        if shifts is None:
            try:
                shifts = self.entries["shifts"]
            except KeyError:
                self.logger.error("There is no key 'divitions' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if shifts is not None:        
            if not isinstance(shifts, list):
                self.logger.error("The supplied 'shifts' is not a list. "
                                  "Exiting.")
                sys.exit(1)
            else:
                for element in shifts:
                    if not isinstance(element, float):
                        self.logger.error("Element: " + str(element) +
                                          "is not a float. Exiting.")
                        sys.exit(1)

    def _check_tetra_volume(self, volume = None):
        """Check that the volume of the tetrahedron is  
        either None or a float.
        
        Parameters
        ----------
        volume : float
            The volume to be checked. If not supplied, the
            volume for the current instance is checked.

        """

        if volume is None:
            try:
                volume = self.entries["tetra_volume"]
            except KeyError:
                self.logger.error("There is no key 'divitions' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if volume is not None:        
            if not isinstance(volume, float):
                self.logger.error("The supplied 'tetra_volume' is not a float. "
                                  "Exiting.")
                        
    def _check_divisions(self, divisions = None):
        """Check that the divisions are either None or
        a list of three integers.
        
        Parameters
        ----------
        divisions : list, optional
            The divisions to be checked. If not supplied, the
            divisions for the current instance is checked.

        """

        if divisions is None:
            try:
                divisions = self.entries["divisions"]
            except KeyError:
                self.logger.error("There is no key 'divitions' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if divisions is not None:        
            if not isinstance(divisions, list):
                self.logger.error("The supplied 'divisions' is not a list. "
                                  "Exiting.")
                sys.exit(1)
            else:
                for element in divisions:
                    if not isinstance(element, int):
                        self.logger.error("Element: " + str(element) +
                                          "is not an integer. Exiting.")
                        sys.exit(1)

    def _check_tetra(self, tetra = None):
        """Check that tetra are either None or
        a list of four integers.
        
        Parameters
        ----------
        tetra : list, optional
            The tetra to be checked. If not supplied, the
            tetra for the current instance is checked.

        """

        if tetra is None:
            try:
                tetra = self.entries["tetra"]
            except KeyError:
                self.logger.error("There is no key 'divisions' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if tetra is not None:        
            if not isinstance(tetra, list):
                self.logger.error("The supplied 'tetra' is not a list. "
                                  "Exiting.")
                sys.exit(1)
            else:
                for element in tetra:
                    if not isinstance(element, list):
                        self.logger.error("An entry in the 'tetra' list is not "
                                          "a list. Exiting.")
                        sys.exit(1)
                    if len(element) != 5:
                        self.logger.error("The 'tetra' elements is not "
                                          "composed of five integers. Exiting.")
                        sys.exit(1)
                    for entry in element:
                        if not isinstance(entry, int):
                            self.logger.error("Entry: " + str(entry) +
                                              " is not an integer. Exiting.")
                            sys.exit(1)
                            
    def _check_centering(self, centering = None):
        """Check that the centering flag is valid.

        Parameters
        ----------
        centering : str, optional
            The centering flag to be checked. If not supplied,
            the centering flag of the current instance is checked.

        """

        if centering is None:
            try:
                centering = self.entries["centering"]
            except KeyError:
                self.logger.error("There is no key 'centering' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if centering is not None:
            # allow None
            if not (centering == "Gamma" or centering == "Monkhorst-Pack"):
                self.logger.error("The supplied 'centering' have to be either "
                                  "Gamma or Monkhorst-Pack. Exiting.")
                sys.exit(1)

    def _check_num_kpoints(self, num_kpoints = None):
        """Check that num_kpoints is valid.

        Parameters
        ----------
        num_kpoints : int, optional
            The num_kpoints to be checked. If not supplied, the 
            num_kpoints of the current instance is checked.

        """

        if num_kpoints is None:
            try:
                num_kpoints = self.entries["num_kpoints"]
            except KeyError:
                self.logger.error("There is no key 'num_kpoints' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if not isinstance(num_kpoints, int):
            self.logger.error("The 'num_kpoints' need to be an integer. "
                              "Exiting.")
            sys.exit(1)
            
    def _check_mode(self, mode = None):
        """Check that the mode flag is valid.

        Parameters
        ----------
        mode : str, optional
            The mode flag to be checked. If not supplied,
            the mode flag of the current instance is checked.

        """

        if mode is None:
            try:
                mode = self.entries["mode"]
            except KeyError:
                self.logger.error("There is no key 'mode' in "
                                  "'entries'. Exiting.")
                sys.exit(1)
        if mode is not None:
            if not ((mode == "explicit") or (mode == "automatic") \
               or (mode == "line")):
                self.logger.error("The supplied 'mode' have to be either "
                                  "explicit, automatic or line-mode. Exiting.")
                sys.exit(1)
                            
    def _validate(self):
        """Validate the content of entries

        """

        self._check_dict()
        self._check_comment()
        self._check_points()
        self._check_centering()
        self._check_divisions()
        self._check_shifts()
        self._check_mode()
        self._check_num_kpoints()
        self._check_tetra()
        self._check_tetra_volume()

    def _to_direct(self, point):

        return point

    def _to_cart(self, point):

        return point
        
    def get(self, tag):
        """Return the value and comment of the entry with tag.

        Parameters
        ----------
        tag : string
            The entry tag of the KPOINTS entry.        

        Returns
        -------
        value : string, int, float or list
            The value of the tag entry

        """

        value = None
        try:
            value = self.entries[tag].get_value()
        except KeyError:
            pass

        return value

    def get_dict(self):
        """Get a true dictionary containing the entries in an
        KPOINTS compatible fashion.

        Returns
        -------
        kpoints_dict : dict
            A dictionary on KPOINTS compatible form.

        """
        
        dictionary = {}
        for key, entry in self.entries.iteritems():
            if key == 'points':
                if entry is not None:
                    dictionary[key] = [[element.get_point(),
                                        element.get_weight(),
                                        element.get_direct()]  for element in entry]
                else:
                    dictionary[key] = None
            else:
                dictionary[key] = entry

        return dictionary

    def get_string(self):
        """Get a string containing the entries in a KPOINTS
        compatible fashion. Each line is broken by a newline
        character

        Returns
        -------

        kpoints_string : str
            A string containing the KPOINTS entries of the
            current instance.

        """
        
        string_object = StringIO.StringIO()
        self._write(kpoints = string_object)
        kpoints_string = string_object.getvalue()
        string_object.close()

        return poscar_string
        
    def write(self, file_path):
        """ Write KPOINTS like files

        Parameters
        ----------
        file_path : str
            The location and filename of the KPOINTS like file to be
            written.

        """

        kpoints = utils.file_handler(file_path, status='w')
        self._write(kpoints = kpoints)
        utils.file_handler(file_handler=kpoints)        
        
    def _write(self, kpoints):
        """ Write KPOINTS like files to a file or string

        Parameters
        ----------
        kpoints : object
            Either a file object or a StringIO object.

        """

        self._validate()
        entries = self.entries
        comment = entries["comment"]
        if comment is None:
            comment = "# \n"
        else:
            comment = "# " + comment
        kpoints.write(comment)
        # check mode
        mode = entries["mode"]
        if mode == "explicit":
            kpoints.write(str(entries["num_kpoints"]) + "\n")
            # points should already be direct
            kpoints.write("Direct\n")
            for point in entries["points"]:
                coordinate = point.get_point()
                kpoints.write(str(coordinate[0]) + " " +
                              str(coordinate[1]) + " " +
                              str(coordinate[2]) + " " +
                              "\n")
            if entries["tetra"] is not None:
                kpoints.write("Tetrahedra\n")
                tetra = entries["tetra"]
                kpoints.write(str(len(tetra)) + " " +
                            str(entries["tetra_volume"]) + "\n")
                for element in tetra:
                    kpoints.write(str(element[0]) + " " +
                                  str(element[1]) + " " +
                                  str(element[2]) + " " +
                                  str(element[3]) + "\n")
        if mode == "automatic":
            kpoints.write("0\n")
            kpoints.write(entries["centering"] + "\n")
            divisions = entries["divisions"]
            kpoints.write(str(divisions[0]) + " " +
                          str(divisions[1]) + " " +
                          str(divisions[2]) + "\n")
            shifts = entries["shifts"]
            if shifts is not None:
                kpoints.write(str(shifts[0]) + " " +
                              str(shifts[1]) + " " +
                              str(shifts[2]) + "\n")

        if mode == "line":
            kpoints.write(str(entries["num_kpoints"])+"\n")
            kpoints.write("Line-mode\n")
            # assume points to be direct
            kpoints.write("Reciprocal\n")
            complete_set = 1
            for index, point in enumerate(entries["points"]):
                coordinate = point.get_point()
                kpoints.write(str(coordinate[0]) + " " +
                              str(coordinate[1]) + " " +
                              str(coordinate[2]) + "\n")
                if complete_set == 2:
                    kpoints.write("\n")
                    complete_set = 0
                complete_set = complete_set + 1
        # remove newline at the end
        utils.remove_newline(kpoints)


class Kpoint(object):

    def __init__(self, point, weight, direct = True, logger=None):
        """A site, typically a position in POSCAR.

        Parameters
        ----------
        point : ndarray
            A kpoint as a ndarray of floats.
        weight : float
            The weight of the given point.
        direct : bool, optional
            True if the kpoint is in direct coordinates. This is the
            default.
        logger : object, optional
            A standard Python logger object.

        """

        if logger is None:
            logger = logging.getLogger(__name__)
        self.logger = logger

        self.point = point
        self.weight = weight
        self.direct = direct

    def get_point(self):
        return self.point

    def get_weight(self):
        return self.weight
    
    def get_direct(self):
        return self.direct
