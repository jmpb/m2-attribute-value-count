# Magento 2 attribute value count
There was a need for us to see which values were not being used and clean up our attributes in our store.

Given an exported list of Magento 2 attributes and values, as well as a product export with the concerned attributes:
This script counts the uses of an attribute value on products and returns a report containing: attribute, value, use count and the skus of the products which are using the value.

An example of the output is in the file `unused_attribute_value.csv`.

As well as our use of cleaning up a Magento store's attribute values - where a further script on the store can be used to iterate and remove the unused attributes, this script can also be used to give a quick report of the usage in CSV format.
