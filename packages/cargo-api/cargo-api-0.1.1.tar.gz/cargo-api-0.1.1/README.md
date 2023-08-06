# Cargo API

Cargo API is a very small package that provides a few convenience functions in regards to error handling in the API.

```python
def SomeExampleEndpoint(self, request, context):
    res = get_response(util_pb2.StandardResponse())

    vr = validate_email(request.email)
    handle_validation_result(res, vr, 'email')
    
    vr = validate_name(request.name)
    handle_validation_result(res, vr, 'name')
    
    if has_errors(res):
        return res
    
    # Do something with the validated data

    return res
```

It offers a standardized validation result object that can be used by any validation function we are using in a specific service. All the other functions now how to deal with the validation result and/or a response object. So you can just run each validation and combine it with a little handler function. After validating everything you check the response object for errors. If there are errors, you stop the flow and send back the errors. Otherwise you have validated input at that point.