
<html>
<body>

## Loop over the databases which are inputted
% for tbl in db:

<h1>From ${tbl.source} (named: ${tbl.name})</h1>

## The JSON databases contain a list of persons, iterate over them
% for person in tbl.data:

## A person is a dictionary with some key-value pairs: convert them to html tags
<h2>${person['friendlyname']}</h2>
<p>${person['firstname']} ${person['lastname']} lives in ${person['address']}, ${person['city']}.</p>

% endfor

% endfor

</body>
</html>

