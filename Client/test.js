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

let sql = "select tag, locks from alltag where tag = ?";
let tag = 'greeting'

connection.query(sql, [tag], function(err, rows){
    if (err) {
        console.log(err)
        return;
    }
    console.log(rows)
});