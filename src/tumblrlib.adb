with Ada.Characters.Handling;
with Ada.Text_IO;
with Ada.Wide_Text_IO;
with GNAT.Sockets;   use GNAT.Sockets;
with Ada.Strings.Unbounded;   use Ada.Strings.Unbounded;
with Ada.Streams;
use type Ada.Streams.Stream_Element_Count;

package body tumblrlib is

   function get_value(S : chars_ptr) return String is
   begin
       if S = Null_Ptr then return "";
       else return Value(S);
      end if;
   end get_value;
   pragma Inline(get_value);

	function post_text(params: chars_ptr; content_length: Integer)
   return Integer
   is
      EOL: String := (1 => ASCII.CR, 2 => ASCII.LF);
      client: Socket_Type;
      address: Sock_Addr_Type;
      channel: Stream_Access;
      offset: Ada.Streams.Stream_Element_Count;
      data: Ada.Streams.Stream_Element_Array (1 .. 256);
	begin
      GNAT.Sockets.Initialize;
      Create_Socket(client);
      address.Addr := Addresses(Get_host_by_name("www.tumblr.com"));
      address.Port := 80;
      Connect_Socket (Client, Address);
      Channel := Stream (Client);
   
      String'Write (Channel, "POST /api/write HTTP/1.1" & EOL);
      String'Write (Channel, "Host: www.tumblr.com" & EOL);
      String'Write (Channel, "Accept-Encoding: identity" & EOL);
      String'Write (Channel, "Content-Length: "& content_length'Img & EOL);
      String'Write (Channel, "Content-type: application/x-www-form-urlencoded" & EOL);
      String'Write (Channel, "Accept: text/plain" & EOL & EOL);
      String'Write (channel, get_value(params));
      Ada.Streams.Read (channel.All, data, offset);
      declare
         chunk: Character;
         reading: Boolean := False;
         status: String := "   ";
         status_index: Integer := 1;
      begin
         for i in 1 .. offset loop
            chunk := Character'Val(data(i));
            exit when chunk = ASCII.CR;
            if reading and chunk = ' ' then
               exit;
            elsif reading then
               status(status_index) := chunk;
               status_index := status_index + 1;
            elsif chunk = ' ' then
               reading := True;
            end if;
         end loop;
         return Integer'Value(status);
      end;
	end post_text;

function validate_credentials(credentials: chars_ptr)
   return Integer
   is
      EOL: String := (1 => ASCII.CR, 2 => ASCII.LF);
      client: Socket_Type;
      address: Sock_Addr_Type;
      channel: Stream_Access;
      offset: Ada.Streams.Stream_Element_Count;
      data: Ada.Streams.Stream_Element_Array (1 .. 256);
      content_length: Integer := 0;
	begin
      GNAT.Sockets.Initialize;
      Create_Socket(client);
      address.Addr := Addresses(Get_host_by_name("www.tumblr.com"));
      address.Port := 80;
      Connect_Socket (Client, Address);
      Channel := Stream (Client);

      content_length := get_value(credentials)'Length;
      
      String'Write (Channel, "POST /api/authenticate HTTP/1.1" & EOL);
      String'Write (Channel, "Host: www.tumblr.com" & EOL);
      String'Write (Channel, "Accept-Encoding: identity" & EOL);
      String'Write (Channel, "Content-Length: "& content_length'Img & EOL);
      String'Write (Channel, "Content-type: application/x-www-form-urlencoded" & EOL);
      String'Write (Channel, "Accept: text/plain" & EOL & EOL);
      String'Write (channel, get_value(credentials));
      Ada.Streams.Read (channel.All, data, offset);
      declare
         chunk: Character;
         reading: Boolean := False;
         status: String := "   ";
         status_index: Integer := 1;
      begin
         for i in 1 .. offset loop
            chunk := Character'Val(data(i));
            exit when chunk = ASCII.CR;
            if reading and chunk = ' ' then
               exit;
            elsif reading then
               status(status_index) := chunk;
               status_index := status_index + 1;
            elsif chunk = ' ' then
               reading := True;
            end if;
         end loop;
         return Integer'Value(status);
      end;
	end validate_credentials;
end tumblrlib;
