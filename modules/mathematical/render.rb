#!/usr/local/bin/ruby -W0

require 'mathematical'
require 'base64'
require 'socket'

math = Mathematical.new({:format => :png, :ppi => 150.0})

while true
    inp = gets
    binary = math.render("$$" + inp + "$$")[:data]
    base64 = Base64.encode64(binary)
    base64.gsub! "\n", ""
    p base64
end