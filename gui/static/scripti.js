function func(str) {
    if (str === "moore") {
        var w = document.getElementById('state_container');
        var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
        var a = document.createElement("div");
        a.classList.add("form-inline", "mb-3");
        a.setAttribute('name', val);
        a.setAttribute('id', "moore_" + val);
        var state_name = document.createElement("input");
        state_name.type = "text";
        state_name.placeholder = "State Name";
        state_name.name = "state_name" + val;
        state_name.classList.add("form-control");
        a.appendChild(state_name);
        var sp = document.createElement("span");
        sp.innerText = " gives ";
        sp.classList.add("ml-2", "mr-2");
        a.appendChild(sp);
        var state_out = document.createElement("input");
        state_out.type = "text";
        state_out.placeholder = "State Output";
        state_out.name = "state_output" + val;
        state_out.classList.add("form-control");
        a.appendChild(state_out);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "Delete";
        cancel.setAttribute('name', "cancel" + val);
        cancel.setAttribute("onclick", "cancel('" + cancel.name + "')");
        cancel.classList.add("btn", "btn-danger", "form-control", "ml-2");
        a.appendChild(cancel);
        w.appendChild(a);
    }
    else {
        var w = document.getElementById('mstate_container');
        var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
        var a = document.createElement("div");
        a.setAttribute('name', val);
        a.classList.add("form-inline", "mb-3");
        a.setAttribute('id', "mealy_" + val);
        var state_name = document.createElement("input");
        state_name.type = "text";
        state_name.placeholder = "State Name";
        state_name.name = "mstate_name" + val;
        state_name.classList.add("form-control");
        a.appendChild(state_name);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "Delete";
        cancel.setAttribute('name', "mcancel" + val);
        cancel.setAttribute("onclick", "cancel('" + cancel.name + "')");
        cancel.classList.add("btn", "btn-danger", "form-control", "ml-2");
        a.appendChild(cancel);
        w.appendChild(a);
    }
}

function funci(str) {
    if (str === "moore") {
        var w = document.getElementById('transition_container');
        var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
        var a = document.createElement("div");
        a.setAttribute('name', val);
        a.setAttribute('id', "tmoore_" + val);
        a.classList.add("form-inline", "mb-3");
        var state = document.createElement("input");
        state.type = "text";
        state.placeholder = "State Name";
        state.name = "state" + val;
        state.classList.add("form-control");
        a.appendChild(state);
        var sp = document.createElement("span");
        sp.innerText = " to ";
        sp.classList.add("ml-2", "mr-2");
        a.appendChild(sp);
        var next_state = document.createElement("input");
        next_state.type = "text";
        next_state.placeholder = "Next State";
        next_state.name = "next_state" + val;
        next_state.classList.add("form-control");
        a.appendChild(next_state);
        var spa = document.createElement("span");
        spa.innerText = " on ";
        spa.classList.add("ml-2", "mr-2");
        a.appendChild(spa);
        var input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Input Value";
        input.name = "input" + val;
        input.classList.add("form-control");
        a.appendChild(input);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "Delete";
        cancel.setAttribute('name', "tcancel" + val);
        cancel.setAttribute("onclick", "cancel('" + cancel.name + "')");
        cancel.classList.add("btn", "btn-danger", "form-control", "ml-2");
        a.appendChild(cancel);
        w.appendChild(a);
    }
    else {
        var w = document.getElementById('mtransition_container');
        var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
        var a = document.createElement("div");
        a.setAttribute('name', val);
        a.setAttribute('id', "tmealy_" + val);
        a.classList.add("form-inline", "mb-3");
        var state = document.createElement("input");
        state.type = "text";
        state.placeholder = "State Name";
        state.name = "mstate" + val;
        state.classList.add("form-control");
        a.appendChild(state);
        var sp = document.createElement("span");
        sp.innerText = " to ";
        sp.classList.add("ml-2", "mr-2");
        a.appendChild(sp);
        var next_state = document.createElement("input");
        next_state.type = "text";
        next_state.placeholder = "Next State";
        next_state.name = "mnext_state" + val;
        next_state.classList.add("form-control");
        a.appendChild(next_state);
        var spa = document.createElement("span");
        spa.innerText = " on ";
        spa.classList.add("ml-2", "mr-2");
        a.appendChild(spa);
        var input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Input Value";
        input.name = "minput" + val;
        input.classList.add("form-control");
        a.appendChild(input);
        var sp1 = document.createElement("span");
        sp1.innerText = " gives ";
        sp1.classList.add("ml-2", "mr-2");
        a.appendChild(sp1);
        var output = document.createElement("input");
        output.type = "text";
        output.placeholder = "Input Value";
        output.name = "moutput" + val;
        output.classList.add("form-control");
        a.appendChild(output);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "Delete";
        cancel.setAttribute('name', "tmcancel" + val);
        cancel.setAttribute("onclick", "cancel('" + cancel.name + "')");
        cancel.classList.add("btn", "btn-danger", "form-control", "ml-2");
        a.appendChild(cancel);
        w.appendChild(a);
    }
}

function select_type() {
    var d = document.getElementById('select');
    if (d.value === "Moore") {
        var m1 = document.getElementById('moore');
        m1.style.display = 'block';
        var m2 = document.getElementById('mealy');
        m2.style.display = 'none';
    }
    else {
        var m1 = document.getElementById('moore');
        m1.style.display = 'none';
        var m2 = document.getElementById('mealy');
        m2.style.display = 'block';
    }
}

function cancel(argument) {
    var a = "";
    console.log(argument);
    if ("cance" === argument.slice(0, 5))
        a = "moore_" + argument.charAt(6);
    else if ("mcanc" === argument.slice(0, 5))
        a = "mealy_" + argument.charAt(7);
    else if ("tcanc" === argument.slice(0, 5))
        a = "tmoore_" + argument.charAt(7);
    else
        a = "tmealy_" + argument.charAt(8);
    console.log(a);
    a.toString();
    var element = document.getElementById(a);
    element.remove();
}

function add_constraints() {
    var doc = document.getElementById("constraints");
    if (doc.style.display === "none") {
        doc.style.display = "block";
        doc.getElementByTagName("button").innerText = "Remove Constraints";
    }
    else {
        doc.style.display = "none";
        doc.getElementByTagName("button").innerText = "Add Constraints";
    }

}

function display_d() {
    var w = document.getElementById("display");
    if (w.innerText === "Add Constraints") {
        document.getElementById("seq_constraints_container").style.display = "block";
        w.innerText = "Remove Constraints";
    }
    else {
        document.getElementById("seq_constraints_container").style.display = "none";
        w.innerText = "Add Constraints";
    }
}

function halwa(argument) {
    if (argument.slice(0, 6) === "BUTTON") {
        document.getElementById(argument.slice(6,)).placeholder = "M or L or R or U or D";
    }
    else {
        document.getElementById(argument.slice(6,)).placeholder = "Number";
    }
}