"""Contains the material class."""

import pygaps

from ..utilities.exceptions import ParameterError


class Material():
    """
    An unified descriptor for an adsorbent material.

    Its purpose is to store properties such as adsorbent name,
    and batch.

    Parameters
    ----------
    name : str
        The name of the material.
    batch : str, None
        A batch number or secondary identifier for the material.

    Other Parameters
    ----------------
    density : float
        Material density.
    molar_mass : float
        Material molar mass.

    Notes
    -----
    The members of the properties are left at the discretion
    of the user. There are, however, some unique properties
    which can be set as seen above.

    """
    def __init__(self, name, **properties):
        """Instantiate by passing all the parameters."""
        #: Material name
        self.name = name

        #: Rest of material properties
        self.properties = properties

    def __repr__(self):
        """Print material name."""
        return self.name

    def __str__(self):
        """Print a short summary of all the material parameters."""
        string = f"pyGAPS Material: {self.name}\n"

        if self.properties:
            for prop in self.properties:
                string += (prop + ':' + str(self.properties.get(prop)) + '\n')

        return string

    def __hash__(self):
        """Override hashing as a hash of name."""
        return hash(self.__repr__())

    def __eq__(self, other):
        """Overload equality operator to use name."""
        if isinstance(other, Material):
            return self.name == other.name
        return self.__repr__() == other

    @classmethod
    def find(cls, material_name):
        """
        Get the material from the master list using its name.

        Parameters
        ----------
        material_name : str
            The name of the material to search.

        Returns
        -------
        Material
            Instance of class.

        Raises
        ------
        ``ParameterError``
            If it does not exist or cannot be calculated.
        """
        # Checks to see if material exists in master list
        material = next((
            material for material in pygaps.MATERIAL_LIST
            if material_name == material.name
        ), None)

        if material is None:
            raise ParameterError(
                f"Material {material_name} does not exist in list of materials. "
                "First populate pygaps.MATERIAL_LIST with required material class"
            )

        return material

    def to_dict(self):
        """
        Return a dictionary of the material class.

        Is the same dictionary that was used to create it.

        Returns
        -------
        dict
            Dictionary of all parameters.

        """
        parameters_dict = {'name': self.name}

        parameters_dict.update(self.properties)

        return parameters_dict

    def get_prop(self, prop):
        """
        Return a property from the internal dictionary.

        Parameters
        ----------
        prop : str
            Property name desired.

        Returns
        -------
        str/float
            Value of property in the properties dict.

        Raises
        ------
        ``ParameterError``
            If it does not exist.

        """
        req_prop = self.properties.get(prop)
        if req_prop is None:
            try:
                req_prop = getattr(self, prop)
            except AttributeError:
                raise ParameterError(
                    f"The {prop} entry was not found in the "
                    f"material properties for material {self.name}."
                )

        return req_prop
