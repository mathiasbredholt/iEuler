#!/usr/local/bin/ruby -W0

require 'mathematical'
require 'base64'
require 'socket'

math = Mathematical.new({:format => :png, :ppi => 120.0})

File.open('out.png', 'wb') { |file|
    file.write(math.render("$$" + ARGV[0] + "$$")[:data])
}
