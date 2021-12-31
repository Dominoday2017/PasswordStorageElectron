let $ = require('jquery')
const {spawn} = require('child_process')
let fs = require('fs')

// RUNTIME 

$('#notify_label').hide()
$('#notify_label_table').hide()

//------NEW POSITION SECTION------

// TAKE NEW POSITION

$('.add_data_btn').on('click', () => {
    let name = $('#name_input').val()
    let email = $('#email_input').val()
    let password = $('#password_input').val()
    let other = $('#other_input').val()
    
    if(name == '' || email == '' || password == ''){
        $('#notify_label').text('This input cant be empty!').show(0).delay(5000).fadeOut(1000)
        if(name == '')
            $('#name_input').css("border", '2px solid red')
        else
            $('#name_input').removeAttr('style')
        if(email == '')
            $('#email_input').css("border", '2px solid red')
        else
            $('#email_input').removeAttr('style')
        if(password == '')
            $('#password_input').css("border", '2px solid red')
        else
            $('#password_input').removeAttr('style')
    }else{
        $('#notify_label').hide()
        $('.input_data').removeAttr('style')

        if(check_input_str(name) == true || check_input_str(email) == true || check_input_str(password) == true || check_input_str(other) == true){
            $('#notify_label').text('Input value cant include "//"').show(0).delay(4000).fadeOut(1000)
        }else{
            to_file(name, email, password, other)
            clear_input()
            get_data_file() 
            $('#notify_label').text('Added new row').show(0).delay(2000).fadeOut(1000)
        }
    }
})

function check_input_str(text){
    if(text.includes("//")){
        return true
    }else
        return false
}
// SAVE ROW TO FILE

function to_file(name, email, password, other){
    const child_python = spawn('python', ['python_scripts/new_row.py', name, email, password, other])

    // PYTHON SYSTEM

    child_python.stdout.on('data', (data) => {
        //console.log(`stdout: ${data}`)
        $('#notify_label').text('This position name alredy exists.').show(0).delay(3000).fadeOut(1000)
    })

    child_python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`)
    })

    child_python.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
    })
}

function clear_input(){
    $('#name_input').val('')
    $('#email_input').val('')
    $('#password_input').val('')
    $('#other_input').val('')
}

//------TABLE SECTION------

// TAKE DATA FROM FILE

function get_data_file(){
    $("#myTable tr").remove(); 
    $('#myTable > tbody:last-child').append('<tr><td class="header">Name</td><td class="header">Email</td><td class="header">Password</td><td class="header">Other</td><td class="header">Delete</td></tr>')
    const child_python = spawn('python', ['python_scripts/read_table.py'])

    // PYTHON SYSTEM

    child_python.stdout.on('data', (data) => {
        output = ''
        output += data.toString()
        display_data(output)
    })

    child_python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`)
    })

    child_python.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
    })
}

// DISPLAY DATA IN TABLE

function display_data(data){
    data = data.split('\n')
    data.forEach((line, index) => {
        if(line != ''){
            let [ name, email, password, other ] = line.split(',')
            $('#myTable > tbody:last-child').append('<tr><td>'
                                                    + name+'</td><td>' 
                                                    + email + '</td><td>' 
                                                    + '<input class="password_label" id="'+ name + '" type="password" value="' + password + '" style="width:auto;"></input>' +'</td><td>' 
                                                    + other +'</td><td>' 
                                                    + '<a class="show_btn" id="' + name + '">&#128065;</a><a class="del_btn" id="' + name + '">&#10006</a><a class="edit_btn" id="' + name + '">&#x270E;</a>' 
                                                    + '</td></tr>');
        }
        
    })   
}

// RELOAD TABLE

$('.reload_btn').on('click', () => {
    get_data_file()
})

// SHOW/HIDE PASSWORD IN TABLE ROW

$('#myTable tbody').on('click', '.show_btn', function() {
    let id = $(this).attr('id')
    let type = $('#' + id).attr("type"); 

    if( type === 'password' ){
        $('#' + id).attr("type", "text");
    }else{
        $('#' + id).attr("type", "password");
    } 
})

// SHOW/HIDE PASSWORD IN ALL TABLE

$('.show_pass_btn').on('click', () => {
    let type = $('.password_label').attr("type")
    if(type === 'password'){
        $('.password_label').attr('type', 'text')
    }else{
        $('.password_label').attr('type', 'password')
    }
})

// DELETE ROW FROM TABLE

$('#myTable tbody').on('click', '.del_btn' ,function() {
    let id = $(this).attr('id')
    delete_row(id)
})

function delete_row(row_id){
    $('#notify_label_table').hide()
    const child_python = spawn('python', ['python_scripts/delete_row.py', row_id])

    // PYTHON SYSTEM

    child_python.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`)
    })

    child_python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`)
    })

    child_python.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
        get_data_file()
    })
    $('#notify_label_table').text("deleted: " + row_id).show(0).delay(1500).fadeOut(500)
}

// EDIT ROW

$('#myTable tbody').on('click', '.edit_btn' , function() {
    let id = $(this).attr('id') // my id 
    fs.writeFile('id_keeper', '')
    fs.writeFile('id_keeper', id)

    let win = window.open('edit_row.html', '_blank', 'width=400,height=450,frame=false,nodeIntegration=yes')
})

// VALUES FROM edit_row.html

$('#confirm_btn').on('click', function() {
    new_name = $('#name').val()
    new_email = $('#email').val()
    new_password = $('#password').val()
    new_other = $('#other').val()
    id = fs.readFileSync('id_keeper', 'utf-8')

    if(new_name == '' && new_email == '' && new_password == '' && new_other == ''){
        alert("Nothing to edit!")
        
    }else{
        edit_row(id, new_name, new_email, new_password, new_other)
    }
})

function edit_row(id, name, email, password, other){
    const child_python = spawn('python', ['python_scripts/edit_row.py', id, name, email, password, other])

    // PYTHON SYSTEM

    child_python.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`)
    })

    child_python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`)
    })

    child_python.on('close', (code) => {
        console.log(`child process exited with code ${code}`)
        alert("Successfully edited. Now you can reload table.")
        window.close()
    })
}

$('#cancel_btn').on('click', () => {
    window.close()
})
// FIND VALUE

$("#position_input").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

get_data_file()