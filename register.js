let $ = require('jquery')
const {spawn} = require('child_process')

$('.submit').on('click', () => {
    let username = $('.un').val()
    let password = $('.pass').val()
    if(username == "" || password == ""){
        alert("username or password cant be empty")
    }else{
        saveToFile_python(username, password)
        $('.un').val('');
        $('.pass').val('');
        alert('register ended successfully')
        destroy()
        window.location.href = "login.html"; //best!
    }
})

function saveToFile_python(username, password){
    const child_python = spawn('python', ['python_scripts/register.py', username, password])
    
    // PYTHON SYSTEM

    child_python.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`)
    })

    child_python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`)
    })

    child_python.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
    })
}

function destroy(){
    const child_python = spawn('python', ['python_scripts/destroy_data.py'])
    
    // PYTHON SYSTEM

    child_python.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
    })
}