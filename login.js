let $ = require('jquery')
const {spawn} = require('child_process')

$('.submit').on('click', () => {
    read_login()
})

function read_login(){
    const child_python = spawn('python', ['python_scripts/login.py'])
    let output = ''
    
    child_python.stdin.setDefaultEncoding = 'utf-8'

    child_python.stdout.on('data', (data) => {
        output += data.toString()
        let [password, username] = output.split(' ')

        if(username == $('.un').val() && password == $('.pass').val() ){
            console.log("login success")
            window.location.href = "index.html";
        }else{
            console.log("login error")
            alert("wrong input data")
        }
    })
    
    // PYTHON SYSTEM

    child_python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`)
    })

    child_python.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
    })
}