class Page:
    @staticmethod
    def to_dict(class_object, object_list):
        object_dict_list = []
        for item in object_list.items:
            object_dict_list.append(class_object.__to_dict__(item))
        return {
            'total': object_list.total,
            'page': object_list.page,
            'amount_of_pages': object_list.pages,
            'per_page': object_list.per_page,
            'amount_of_next_pages': object_list.next_num,
            'amount_of_previous_pages': object_list.prev_num,
            'objects': object_dict_list
        }