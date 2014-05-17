user = `git config user.name`.strip
email = `git config user.email`.strip

puts "\n# With #{user} <#{email}>"


#puts `git status`.gsub(/# On branch [^\n]*/, '\0' + "\n# with #{user} <#{email}>")
# puts "# On branch master".gsub(/# On branch [^\n]*/, '\0 - ')