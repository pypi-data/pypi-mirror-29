# django-rest-form-fields
Extended form fields to validate REST-request data via django.forms.

## Requirements
* Python 2.7 or Python 3.3+
* Django >= 1.7
* pytz
* jsonschema
* six
* typing

## Installation
Install via pip:  
`pip install django-rest-form-fields`    
or via setup.py:  
`python setup.py install`

## Usage
You can use standard [django forms](https://docs.djangoproject.com/en/1.11/ref/forms/), adding new fields for them.
All `*args` and `**kwargs` fields in reference below will be passed to base django constructors as is.

Example:
```python
from django import forms
from django_rest_form_fields import FileField, ArrayField
    
class MyForm(forms.Form):
    file_field = FileField(max_size=1024, valid_extensions=['valid_extensions'])
    array_field = ArrayField(min_items=1, max_items=10)
            
```

## Fields and their options

### RestCharField(*args, **kwargs)
Wraps django.forms.forms.CharField:
* Changes default value - None, not empty string
* Fixes initial value (CharField returns empty string, ignoring 'initial' parameter and None value)  

Resulting value: `Optional[str]`

### RegExField(*args, regex: Optional[str] = None, flags: int = 0, **kwargs)
RestCharField child class, that automatically validates given string with regex (re.match function)   
If regex parameter is specified and value matches expression, you can get MatchObject using field `match` attribute

Parameters:
* regex: str - regular expression string or compiled with `re.compile()` object
* flags: int - optional validate flags  

Resulting value: `Optional[str]`

### RestChoiceField(*args, choices: Optional[Iterable[Union[str, Tuple[str]]]] = None, **kwargs)
Wraps django.forms.forms.ChoiceField:
* Changes default value - None, not empty string
* Fixes initial value (ChoiceField returns empty string, ignoring 'initial' parameter and None value)
* Gives opportunity to set 'choices' as iterable of values, not iterable of tuples  

Resulting value: `Optional[str]`

### RestIntegerField(*args, **kwargs)
### RestFloatField(*args, **kwargs)
Wrap django.forms.forms.IntegerField and django.forms.forms.FloatField, fixing initial value (Base fields returns None, ignoring 'initial' parameter and None value)  

Resulting value: `Optional[int/float]`

### PositiveIntegerField(*args, with_zero: bool = False, **kwargs)
### IdField(*args, with_zero: bool = False, **kwargs)
Child of RestIntegerField, validating value as positive integer
Parameters:
* with_zero: bool - if False, 0 will cause validation error  

Resulting value: `Optional[int]`

### TimestampField(*args, in_future: bool = True, **kwargs)
Child of RestFloatField. Gets timestamp value and converts it into `datetime.datetime` object in UTC.
Parameter `initial` can be float or `datetime.datetime` value.  
Parameters:
* in_future: bool - if False, datetime is validated to be less than `datetime.datetime.now()`  

Resulting value: `Optional[datetime.datetime]`

### DateTimeField(*args, mask: str = "%Y-%m-%dT%H:%M:%S", **kwargs)
Child of RestCharField. Parses datetime string to `datetime.datetime` value.
Parameters:
* mask: str - template for [datetime.strptime](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior) function  

Resulting value: `Optional[datetime.datetime]`

### MonthField(*args, mask: str = "%Y-%m", **kwargs)
Child of DateTimeField. Parses month string to `datetime.date` value.
Returns date of the first day of the month.
Parameters:
* mask: str - template for [datetime.strptime](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior) function  

Resulting value: `Optional[datetime.date]`

### TimezoneField(*args, **kwargs)
Child of RestCharField. Validates string as one of pytz timezone names.

Resulting value: `Optional[str]`

### DateUnitField(*args, **kwargs)
Child of RestChoiceField, validating value as one of [hour, day, week]  

Resulting value: `Optional[str]`

### RestBooleanField(*args, **kwargs)
Standard `django.forms.forms.BooleanField` is based on /django/forms/widgets.py `CheckboxInput.value_from_datadict(value)`
It works improperly for REST model: `required=True` + `value=False` => `ValidationError`
This filed fixes this issue, giving opportunity to send False (required or not):
* None as default value
* 'false', '0', '' (ignoring case) as False
* Everything else is parsed with standard bool function  

Resulting value: `Optional[str]`

### LowerCaseEmailField(*args, **kwargs)
Wraps `django.forms.forms.EmailField`:
* Converts email string to lowercase
* Fixes initial value bug (EmailField returns empty string, ignoring 'initial' parameter)
* Changes default value - None, not empty string  

Resulting value: `Optional[str]`

### ColorField(*args, **kwargs)
Child of RestCharField, validating color.
Color should be six hexadecimal characters.  

Resulting value: `Optional[str]`

### TruncatedCharField(*args, truncate_length: int = 255, **kwargs)
Child of RestCharField, which truncates given value, leaving first truncate_length characters.
Parameters:
* truncate_length: Optional[int] - If None, acts as RestCharField. If integer - number of characters to leave.  

Resulting value: `Optional[str]`

### JsonField(*args, json_schema: Optional[dict], **kwargs)
Child of RestCharField. Validates, that value is dict, list or JSON-encoded string.
If string - decodes it.
Parameters:
* json_schema: Optional[dict] - Object to validate given JSON with [jsonschema package](https://pypi.python.org/pypi/jsonschema).

Resulting value: `Optional[Any]`

### ArrayField(*args, min_items: int = 0, max_items: Optional[int] = None, item_schema: Optional[dict] = None, **kwargs)
JsonField child. Validates array. It can be represented in 3 forms:
* list instance
* JSON-encoded array
* comma-separated string

Parameters:
* min_items: int - Validates array has more or equal items
* max_items: Optional[int] - Validates array has less or equal items
* item_schema: Optional[dict] - Object to validate every item with [jsonschema package](https://pypi.python.org/pypi/jsonschema).  

Resulting value: `Optional[List[Any]]`

### IdArrayField(*args, **kwargs)
ArrayField child. Validates array of IdField().  
Each array element is cleaned with IdField().  

Resulting value: `Optional[List[int]]`

### IdSetField(*args, **kwargs)
IdArrayField child. Validates set of IdField().  
Each element is cleaned with IdField(). Removes duplicated ids from input, if needed.  

Resulting value: `Optional[Set[int]]`

### UrlField(*args, **kwargs)
RestCharField child. Validates string as URL with `django.core.validators.URLValidator`

Resulting value: `Optional[str]`

### HexField(*args, **kwargs)
RestCharField child. Validates that string has hexadecimal characters only.

Resulting value: `Optional[str]`

### UUIDField(*args, **kwargs)
RegexField child. Validates field to be correct UUID.

Resulting value: `Optional[str]`

### FileField(*args, max_size: Optional[int] = None, valid_extensions: Optional[List[str]] = None, **kwargs)
Wraps django.forms.forms.FileField:
* Fixes initial value bug (FileField returns empty string, ignoring 'initial' parameter)
* Adds validation parameters

Parameters:
* max_size: Optional[int] - File size in bytes
* valid_extensions: Optional[List[str]] - file extensions (without .), that are valid

Resulting value: `Optional[file]`