with Interfaces.C.Strings; use Interfaces.C.Strings;
package tumblrlib is
	function post_text(params: chars_ptr; content_length: Integer) return Integer;
	pragma export (C, post_text, "post_text");
	function validate_credentials(credentials: chars_ptr) return Integer;
	pragma export (C, validate_credentials, "validate_credentials");
end tumblrlib;
