from typing import List, Any


class Filter:
    def __init__(self, key: str, values: List[Any]):
        """
        :param key: Class attribute to compare with values
        :param values: Values to compare with key

        Example:
        Filter(key="status", values=["FINISHED", "WAITING"])
        """

        self.key = key
        self.values = values


class FilterJoin:
    def __init__(
            self,
            class_: object,
            class_attr: object,
            join_attr: object,
            values: List[Any] = None,
            class_key: str = "id",
    ):
        """
        :param class_: Class to join
        :param class_attr: Class attribute to compare with join_attr
        :param join_attr: Class attribute to compare with class_attr
        :param values: Values to compare with class_key
        :param class_key: Class attribute to compare with values

        Example:

        # Filter Inspections by Mission id
        FilterJoin(
            class_=Mission,
            class_attr=Mission.inspection_id,
            join_attr=Inspection.id,
            values=[1, 2, 3],
            class_key="id"
        )
        """

        self.class_ = class_
        self.class_attr = class_attr
        self.join_attr = join_attr
        self.values = values
        self.class_key = class_key
