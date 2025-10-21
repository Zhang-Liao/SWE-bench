# marshmallow-code__marshmallow-1164

## 基本信息

- **实例ID**: marshmallow-code__marshmallow-1164
- **仓库**: marshmallow-code/marshmallow
- **版本**: 2.18
- **创建时间**: 2019-03-01T17:03:05Z
- **基础提交**: 1e26d14facab213df5009300b997481aa43df80a
- **环境设置提交**: 1e26d14facab213df5009300b997481aa43df80a

## 问题描述

2.x: Nested(many=True) eats first element from generator value when dumping
As reproduced in Python 3.6.8:

```py
from marshmallow import Schema, fields

class O(Schema):
    i = fields.Int()

class P(Schema):
    os = fields.Nested(O, many=True)

def gen():
    yield {'i': 1}
    yield {'i': 0}

p = P()
p.dump({'os': gen()})
# MarshalResult(data={'os': [{'i': 0}]}, errors={})
```

Problematic code is here:

https://github.com/marshmallow-code/marshmallow/blob/2.x-line/src/marshmallow/fields.py#L447

And here:

https://github.com/marshmallow-code/marshmallow/blob/2.x-line/src/marshmallow/schema.py#L832

The easiest solution would be to cast `nested_obj` to list before calling `schema._update_fields`, just like a normal Schema with `many=True` does.


## 解决方案补丁

Input: nested_obj
Output: list representation of nested_obj

```diff
diff --git a/src/marshmallow/fields.py b/src/marshmallow/fields.py
--- a/src/marshmallow/fields.py
+++ b/src/marshmallow/fields.py
@@ -443,6 +443,8 @@ def _serialize(self, nested_obj, attr, obj):
         schema = self.schema
         if nested_obj is None:
             return None
+        if self.many and utils.is_iterable_but_not_string(nested_obj):
+            nested_obj = list(nested_obj)
         if not self.__updated_fields:
             schema._update_fields(obj=nested_obj, many=self.many)
             self.__updated_fields = True
```
???
**spec:**
Input: obj
Output: if obj is a list, then return its first element, else raise error

```diff
diff --git a/src/marshmallow/schema.py b/src/marshmallow/schema.py
--- a/src/marshmallow/schema.py
+++ b/src/marshmallow/schema.py
@@ -816,23 +816,14 @@ def __filter_fields(self, field_names, obj, many=False):

         :param set field_names: Field names to include in the final
             return dictionary.
+        :param object|Mapping|list obj The object to base filtered fields on.
         :returns: An dict of field_name:field_obj pairs.
         """
         if obj and many:
-            try:  # Homogeneous collection
-                # Prefer getitem over iter to prevent breaking serialization
-                # of objects for which iter will modify position in the collection
-                # e.g. Pymongo cursors
-                if hasattr(obj, '__getitem__') and callable(getattr(obj, '__getitem__')):
-                    try:
-                        obj_prototype = obj[0]
-                    except KeyError:
-                        obj_prototype = next(iter(obj))
-                else:
-                    obj_prototype = next(iter(obj))
-            except (StopIteration, IndexError):  # Nothing to serialize
+            try:  # list
+                obj = obj[0]
+            except IndexError:  # Nothing to serialize
                 return dict((k, v) for k, v in self.declared_fields.items() if k in field_names)
-            obj = obj_prototype
         ret = self.dict_class()
         for key in field_names:
             if key in self.declared_fields:

```

## spec

```py
from marshmallow import Schema, fields

class O(Schema):
    i = fields.Int()

class P(Schema):
    os = fields.Nested(O, many=True)

# Precondition:
# The input argument f is a reference to a function.
# f receives no arguments
# Running f each time yields to an integer.

# Postcondition:
# l is a list obtained by merging all yielded outputs from f.
# The output of test equals to l.
def test(f):
    p = P()
    out = p.dump(f)
    return out
```

## 测试补丁

```diff
diff --git a/tests/test_serialization.py b/tests/test_serialization.py
--- a/tests/test_serialization.py
+++ b/tests/test_serialization.py
@@ -782,3 +782,21 @@ class ValueSchema(Schema):
 
     serialized = ValueSchema(many=True).dump(slice).data
     assert serialized == values
+
+
+# https://github.com/marshmallow-code/marshmallow/issues/1163
+def test_nested_field_many_serializing_generator():
+    class MySchema(Schema):
+        name = fields.Str()
+
+    class OtherSchema(Schema):
+        objects = fields.Nested(MySchema, many=True)
+
+    def gen():
+        yield {'name': 'foo'}
+        yield {'name': 'bar'}
+
+    obj = {'objects': gen()}
+    data, _ = OtherSchema().dump(obj)
+
+    assert data.get('objects') == [{'name': 'foo'}, {'name': 'bar'}]

```

## 测试信息

### 失败的测试 (FAIL_TO_PASS)
["tests/test_serialization.py::test_nested_field_many_serializing_generator"]

### 通过的测试 (PASS_TO_PASS)
["tests/test_serialization.py::TestFieldSerialization::test_default", "tests/test_serialization.py::TestFieldSerialization::test_number[42-42.0]", "tests/test_serialization.py::TestFieldSerialization::test_number[0-0.0]", "tests/test_serialization.py::TestFieldSerialization::test_number[None-None]", "tests/test_serialization.py::TestFieldSerialization::test_number_as_string", "tests/test_serialization.py::TestFieldSerialization::test_number_as_string_passed_none", "tests/test_serialization.py::TestFieldSerialization::test_callable_default", "tests/test_serialization.py::TestFieldSerialization::test_function_field_passed_func", "tests/test_serialization.py::TestFieldSerialization::test_function_field_passed_serialize", "tests/test_serialization.py::TestFieldSerialization::test_function_field_passed_func_is_deprecated", "tests/test_serialization.py::TestFieldSerialization::test_function_field_passed_serialize_with_context", "tests/test_serialization.py::TestFieldSerialization::test_function_field_passed_uncallable_object", "tests/test_serialization.py::TestFieldSerialization::test_integer_field", "tests/test_serialization.py::TestFieldSerialization::test_integer_as_string_field", "tests/test_serialization.py::TestFieldSerialization::test_integer_field_default", "tests/test_serialization.py::TestFieldSerialization::test_integer_field_default_set_to_none", "tests/test_serialization.py::TestFieldSerialization::test_callable_field", "tests/test_serialization.py::TestFieldSerialization::test_uuid_field", "tests/test_serialization.py::TestFieldSerialization::test_decimal_field", "tests/test_serialization.py::TestFieldSerialization::test_decimal_field_string", "tests/test_serialization.py::TestFieldSerialization::test_decimal_field_special_values", "tests/test_serialization.py::TestFieldSerialization::test_decimal_field_special_values_not_permitted", "tests/test_serialization.py::TestFieldSerialization::test_decimal_field_fixed_point_representation", "tests/test_serialization.py::TestFieldSerialization::test_boolean_field_serialization", "tests/test_serialization.py::TestFieldSerialization::test_function_with_uncallable_param", "tests/test_serialization.py::TestFieldSerialization::test_email_field_validates", "tests/test_serialization.py::TestFieldSerialization::test_email_field_serialize_none", "tests/test_serialization.py::TestFieldSerialization::test_dict_field_serialize_none", "tests/test_serialization.py::TestFieldSerialization::test_dict_field_invalid_dict_but_okay", "tests/test_serialization.py::TestFieldSerialization::test_dict_field_serialize", "tests/test_serialization.py::TestFieldSerialization::test_dict_field_serialize_ordereddict", "tests/test_serialization.py::TestFieldSerialization::test_url_field_serialize_none", "tests/test_serialization.py::TestFieldSerialization::test_url_field_validates", "tests/test_serialization.py::TestFieldSerialization::test_method_field_with_method_missing", "tests/test_serialization.py::TestFieldSerialization::test_method_field_with_uncallable_attribute", "tests/test_serialization.py::TestFieldSerialization::test_method_prefers_serialize_over_method_name", "tests/test_serialization.py::TestFieldSerialization::test_method_with_no_serialize_is_missing", "tests/test_serialization.py::TestFieldSerialization::test_serialize_with_dump_to_param", "tests/test_serialization.py::TestFieldSerialization::test_serialize_with_attribute_and_dump_to_uses_dump_to", "tests/test_serialization.py::TestFieldSerialization::test_datetime_serializes_to_iso_by_default", "tests/test_serialization.py::TestFieldSerialization::test_datetime_invalid_serialization[invalid]", "tests/test_serialization.py::TestFieldSerialization::test_datetime_invalid_serialization[value1]", "tests/test_serialization.py::TestFieldSerialization::test_datetime_invalid_serialization[24]", "tests/test_serialization.py::TestFieldSerialization::test_datetime_field_rfc822[rfc]", "tests/test_serialization.py::TestFieldSerialization::test_datetime_field_rfc822[rfc822]", "tests/test_serialization.py::TestFieldSerialization::test_localdatetime_rfc_field", "tests/test_serialization.py::TestFieldSerialization::test_datetime_iso8601[iso]", "tests/test_serialization.py::TestFieldSerialization::test_datetime_iso8601[iso8601]", "tests/test_serialization.py::TestFieldSerialization::test_localdatetime_iso", "tests/test_serialization.py::TestFieldSerialization::test_datetime_format", "tests/test_serialization.py::TestFieldSerialization::test_string_field", "tests/test_serialization.py::TestFieldSerialization::test_formattedstring_field", "tests/test_serialization.py::TestFieldSerialization::test_formattedstring_field_on_schema", "tests/test_serialization.py::TestFieldSerialization::test_string_field_default_to_empty_string", "tests/test_serialization.py::TestFieldSerialization::test_time_field", "tests/test_serialization.py::TestFieldSerialization::test_invalid_time_field_serialization[badvalue]", "tests/test_serialization.py::TestFieldSerialization::test_invalid_time_field_serialization[]", "tests/test_serialization.py::TestFieldSerialization::test_invalid_time_field_serialization[in_data2]", "tests/test_serialization.py::TestFieldSerialization::test_invalid_time_field_serialization[42]", "tests/test_serialization.py::TestFieldSerialization::test_date_field", "tests/test_serialization.py::TestFieldSerialization::test_invalid_date_field_serialization[badvalue]", "tests/test_serialization.py::TestFieldSerialization::test_invalid_date_field_serialization[]", "tests/test_serialization.py::TestFieldSerialization::test_invalid_date_field_serialization[in_data2]", "tests/test_serialization.py::TestFieldSerialization::test_invalid_date_field_serialization[42]", "tests/test_serialization.py::TestFieldSerialization::test_timedelta_field", "tests/test_serialization.py::TestFieldSerialization::test_datetime_list_field", "tests/test_serialization.py::TestFieldSerialization::test_list_field_with_error", "tests/test_serialization.py::TestFieldSerialization::test_datetime_list_serialize_single_value", "tests/test_serialization.py::TestFieldSerialization::test_list_field_serialize_none_returns_none", "tests/test_serialization.py::TestFieldSerialization::test_list_field_respect_inner_attribute", "tests/test_serialization.py::TestFieldSerialization::test_list_field_respect_inner_attribute_single_value", "tests/test_serialization.py::TestFieldSerialization::test_list_field_work_with_generator_single_value", "tests/test_serialization.py::TestFieldSerialization::test_list_field_work_with_generators_multiple_values", "tests/test_serialization.py::TestFieldSerialization::test_list_field_work_with_generators_error", "tests/test_serialization.py::TestFieldSerialization::test_list_field_work_with_generators_empty_generator_returns_none_for_every_non_returning_yield_statement", "tests/test_serialization.py::TestFieldSerialization::test_list_field_work_with_set", "tests/test_serialization.py::TestFieldSerialization::test_list_field_work_with_custom_class_with_iterator_protocol", "tests/test_serialization.py::TestFieldSerialization::test_bad_list_field", "tests/test_serialization.py::TestFieldSerialization::test_serialize_does_not_apply_validators", "tests/test_serialization.py::TestFieldSerialization::test_constant_field_serialization", "tests/test_serialization.py::TestFieldSerialization::test_constant_is_always_included_in_serialized_data", "tests/test_serialization.py::TestFieldSerialization::test_constant_field_serialize_when_omitted", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[String]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Integer]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Boolean]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Float]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Number]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[DateTime]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[LocalDateTime]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Time]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Date]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[TimeDelta]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Dict]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Url]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Email]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[FormattedString]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[UUID]", "tests/test_serialization.py::TestFieldSerialization::test_all_fields_serialize_none_to_none[Decimal]", "tests/test_serialization.py::test_serializing_named_tuple", "tests/test_serialization.py::test_serializing_named_tuple_with_meta", "tests/test_serialization.py::test_serializing_slice"]

## 提示信息

I confirmed that this is no longer an issue in marshmallow 3. I was able to reproduce this with python 2 and 3 using the latest version of marshmallow 2.
`next(iter(...))` is not a safe operation for generators.

```py
def gen():
    yield 1
    yield 2

x = gen()
next(iter(x))
# 1
list(x)
# [2]
```

I suspect `list` would be an acceptable solution. If it was a performance concern we could use `itertools.tee` to copy the generator before peeking at the first item.
`next(iter(...))` is apparently fine because `obj` is guaranteed to be a list here:

https://github.com/marshmallow-code/marshmallow/blob/2.x-line/src/marshmallow/schema.py#L489

It's just that usage of `Schema._update_fileds` in `Nested` ignores the requirement.


---

*此文件由SWE-bench数据自动生成*
*生成时间: 2025-10-20 11:39:41*
