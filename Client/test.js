var mysql = require('mysql');

var connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "chatbot"
});

connection.connect(function(err){
    if (err) {
        console.log(err)
    }
    console.log("OK")
});

$query = "select * from alltag";

connection.query($query, function(err, rows){
    if (err) {
        console.log(err)
        return;
    }
    console.log(rows)
});