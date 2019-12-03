const mysql = require('mysql');
const util = require('util');

const pool = mysql.createPool({
    connectionLimit: 10,
    host: "localhost",
    user: "root",
    password: "",
    database: "chatbot"
});

pool.getConnection((err, connection) => {
    if (err) {
        console.log(err)
    }
    if (connection) connection.release();
    return;
});

pool.query = util.promisify(pool.query);

module.exports = pool;

return module.exports;

