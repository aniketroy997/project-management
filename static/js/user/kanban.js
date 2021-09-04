window.filter_data = ''

$('#closeMessage').click(function(){$('#message_container').hide(0);})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

window.projectList = [];

myProjectsList()
function myProjectsList(){
	var url = '/api/user-project_list/'+userId

	fetch(url)
	.then((resp) => resp.json())
	.then(function(data){
		projectList = data
		var options = ''
		for(var i in projectList){
			options += `<option value="`+projectList[i].id+`">`+projectList[i].title+`</option>`
		}
		
		project_selection_list =
		`
			<div class="collapse" id="collapse-filter">

				<div class="form-row">
					<div class="form-group col-md-3">
						<label for="id_title">Project:</label>
						<select name="dropdown" class="form-control" id="selectedProject">
						<option value="-1">All</option>
						`+ options +`
						</select>
					</div>
				</div>
				<form id="filter_form">
					<div class="form-row">
						<div class="form-group col-md-2">
							<label for="id_title">Title:</label>
							<input type="text" class="form-control" name="title" maxlength="255" id="id_title_filter">
						</div>
						<div class="form-group col-md-2">
							<label for="id_title">Phase:</label>
							<input type="text" class="form-control" name="phase_Id" maxlength="255" id="id_phase_filter">
						</div>
						<div class="form-group col-md-2">
							<label for="id_description">Milestone:</label>
							<input type="text" class="form-control" name="milestone_Id" maxlength="255" id="id_milestone_filter">
						</div>
						<div class="form-group col-md-2">
							<label for="id_date_of_start">Date of start:</label>
							<input type="date" class="form-control" name="start_date" id="id_date_of_start_filter">
						</div>
						<div class="form-group col-md-2">
							<label for="id_date_of_end">Date of end:</label>
							<input type="date" class="form-control" name="end_date" id="id_date_of_end_filter">
						</div>
						<div class="form-group col-md-2 align-self-end">
							<button type="button" class="btn btn-primary" id="filter_button">Filter</button>
							<button type="button" class="btn btn-dark" id="clear_filter_button">Clear</button>
						</div>
					</div>
				</form>
			</div>
		`
		$('#project_selection').append(project_selection_list)
		$('select[id="selectedProject"]').change(function(){
			buildBoardColumns()
		})

		$('select[id="packagetype"]').change(function(){
			clearBoardColumns()
		})
		
		buildBoardColumns()
		filter_functions()
	})
}

function filter_functions(){
	$("#filter_button").click(function(){
		filter_data = $("#filter_form").serialize()
		buildBoardColumns()
	})
	$("#clear_filter_button").click(function(){
		$("#filter_form")[0].reset();
		filter_data =''
		buildBoardColumns()
	})
}

function clearBoardColumns(){

	packageType = $('select[id="packagetype"]').val()
	columnBuilder();
	if(packageType == 1){
		FillBuildedBoardColumns_SWP()
	}
	else if(packageType == 2){
		FillBuildedBoardColumns_WP()
	}
	
}

// Creates the columns in kanban board
function buildBoardColumns(){
	
	columnBuilder();
	FillBuildedBoardColumns_SWP();
	
}
function columnBuilder(){
	var wrapper = document.getElementById('taskCardContainer');
	$("#taskCardContainer").html("")
	var url = '/api/kanban-state/'

	fetch(url)
	.then((resp) => resp.json())
	.then(function(data){

		var kanbanColumns = data

		for(var i in kanbanColumns){	
			
			div = 	document.createElement('div')	
					div.setAttribute('id', "column-"+kanbanColumns[i].id);
					div.setAttribute('data-state', kanbanColumns[i].id);
					div.setAttribute('style', "min-height: 600px;");
					div.classList.add('list')
					div.classList.add('col')
					div.classList.add('rounded-lg')
					div.classList.add('m-1')
					div.classList.add('border')
					div.classList.add('border-dark')
					div.innerHTML =`
					<p>${kanbanColumns[i].title}</p>
					<hr style="background-color:#0091D5;"/>`;
			wrapper.appendChild(div);
		}
	})
}
// fills the card in the required columns of kanban board
function FillBuildedBoardColumns_SWP(){
	project_Id = $('select[id="selectedProject"]').val()
	if(filter_data == '')
	{
		if(project_Id == '-1')
			var url = '/api/subWorkPackages-user-list/'+userId
		else
			var url = '/api/single-subWorkPackages-user-list/'+userId+'/'+ project_Id
	}
	else{
		if(project_Id == '-1')
			var url = '/api/subWorkPackages-user-list/'+userId+'?'+filter_data
		else
			var url = '/api/single-subWorkPackages-user-list/'+userId+'/'+ project_Id+'?'+filter_data
	}

	fetch(url)
	.then((resp) => resp.json())
	.then(function(data){

		var kanbanCards = data
		
		for(var i in kanbanCards){
			
			if(kanbanCards[i].state != null){
				var wrapper = document.getElementById('column-'+kanbanCards[i].state);
				var item = `
				<div class="list-item card" id="${kanbanCards[i].id}" draggable="true" data-id="${kanbanCards[i].id}" data-state="${kanbanCards[i].state}"  style="border-left-width:thick;border-left-color:${kanbanCards[i].border_color}">
					<!--DropDown -->
					<div class="dropdown" data-id = "${kanbanCards[i].id}">
						<button class="btn float-right btn-sm" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
						<i class="fa fa-ellipsis-v text-warning"></i>
						</button>
						<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
							<button data-toggle="modal" data-target="#EditModal" class="editButtonSWPClass dropdown-item btn-sm" data-id="${kanbanCards[i].id}">Edit</button>
							<button class="deleteButtonSWPClass dropdown-item btn-sm" data-id="${kanbanCards[i].id}">Delete</button>
						</div>
					
						<!--/DropDown -->
						<div class="card-body">
							<h6 class="card-title" id="${kanbanCards[i].id}-taskTitle">${kanbanCards[i].title}</h6>
							<small><p class="card-text text-muted" id="${kanbanCards[i].id}-taskDescription">${kanbanCards[i].description}</p></small>
							<small><p class="card-text text-muted" id="${kanbanCards[i].id}-taskProject">Project : ${kanbanCards[i].project_Id}</p></small>
						</div>
					</div>
				</div>
				`
			}
			else{
				var wrapper = document.getElementById('column-1');
				var item = `
				<div class="list-item card" id="${kanbanCards[i].id}" draggable="true" data-id="${kanbanCards[i].id}" data-state="${kanbanCards[i].state}"  style="border-left-width:thick;border-left-color:${kanbanCards[i].border_color}">
					<!--DropDown -->
					<div class="dropdown" data-id = "${kanbanCards[i].id}">
						<button class="btn float-right btn-sm" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
						<i class="fa fa-ellipsis-v text-warning"></i>
						</button>
						<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
							<button data-toggle="modal" data-target="#EditModal" class="editButtonSWPClass dropdown-item btn-sm" data-id="${kanbanCards[i].id}">Edit</button>
							<button class="deleteButtonSWPClass dropdown-item btn-sm" data-id="${kanbanCards[i].id}">Delete</button>
						</div>
					
						<!--/DropDown -->
						<div class="card-body">
							<h6 class="card-title" id="${kanbanCards[i].id}-taskTitle">${kanbanCards[i].title}</h6>
							<small><p class="card-text text-muted" id="${kanbanCards[i].id}-taskDescription">${kanbanCards[i].description}</p></small>
							<small><p class="card-text text-muted" id="${kanbanCards[i].id}-taskProject">${kanbanCards[i].project_Id}</p></small>
						</div>
					</div>
				</div>
				`
			}
			wrapper.innerHTML += item
			
		}
		//making card functionable
		dragFunction()
	})

}