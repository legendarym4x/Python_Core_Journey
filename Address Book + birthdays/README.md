### In this task we:

Let's add a `Birthday` field. This field is optional, but there can be only one.

Let's add the functionality of working with `Birthday` to the Record class, namely the `days_to_birthday` function, which returns the number of days until the next birthday.

We will add a functionality to check the correctness of the given values for the `Phone`, `Birthday` fields.

Let's add pagination (page output) for `AddressBook` for situations when the book is very large and you need to show the content in parts, and not all at once. We implement this by creating an iterator by records.

### Necessary conditions:

`AddressBook` implements an `iterator` method that returns a generator by records and in one iteration returns a representation for N records.

The `Record` class accepts one additional (optional) argument of the Birthday class

The `Record` class implements the days_to_birthday method, which returns the number of days until the contact's next birthday if the birthday is given.

`setter` and `getter` logic for the value attributes of the Field inheritors.

Checking the correctness of the `setter` phone number for the value of the `Phone` class.

Checking the correctness of the managed birthday `setter` for the value of the `Birthday` class.
