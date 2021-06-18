# oauth-redirects
> A simple to capture request information. Mostly for applications that need redirecting when using OAuth2

> [auth.thesammy2010.com](http://auth.thesammy2010.com/?source=GitHub&didYouClick=true) to test it out
# Example Usage

### Request 1
```http
GET /?appid=test&code=1234

Host: auth.thesammy2010.com
User-Agent: python-requests/2.22.0
Accept-Encoding: gzip, deflate
Accept: application/json
Content-Type: application/json
Connection: keep-alive
```
### Response 1

```json
{
    "request_id": "6c0f2c1e-0ca3-4838-b685-fde4a5bc10e7",
    "status_code": 200,
    "result": "Success",
    "errors": [],
    "data": {
	    "appid": "test",
	    "code": "1234"
	}
}
```
### Request 2

```http
POST /

Host: auth.thesammy2010.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
Accept: text/html
Content-Type: application/json
Connection: keep-alive

{
    "key": "value",
    "test": true
}
```
### Response 2
```html
<!DOCTYPE  html>
<html>
	<body>
		<h1>Response</h1>
		<pre>
			<code>
{
    "request_id": "6c0f2c1e-0ca3-4838-b685-fde4a5bc10e7",
    "status_code": 200,
    "result": "Success",
    "errors": [],
    "data": {
        "key": "value",
        "test": true
	}
}
			</code>
		</pre>
	</body>
</html>
```