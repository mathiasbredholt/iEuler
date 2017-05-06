#!/usr/local/bin/ruby -W0

require 'mathematical'
require 'base64'
require 'socket'

math = Mathematical.new({:format => :png, :ppi => 120.0})

File.open(ARGV[0], 'wb') { |file|
    file.write(math.render("$$" + ARGV[1] + "$$")[:data])
}
