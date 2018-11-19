function func(str) {
    if (str === "moore") {
        var w = document.getElementById('state_container');
        var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
        var a = document.createElement("div");
        a.setAttribute('name', val);
        a.setAttribute('id', "moore_" + val);
        var p = document.createElement("p");
        var state_name = document.createElement("input");
        state_name.type = "text";
        state_name.placeholder = "State Name";
        state_name.name = "state_name" + val;
        p.appendChild(state_name);
        var sp = document.createElement("span");
        sp.innerText = " gives ";
        p.appendChild(sp);
        var state_out = document.createElement("input");
        state_out.type = "text";
        state_out.placeholder = "State Output";
        state_out.name = "state_output" + val;
        p.appendChild(state_out);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "cancel";
        cancel.setAttribute('name',"cancel" + val);
        cancel.setAttribute("onclick","cancel('" + cancel.name + "')");
        cancel.setAttribute("class","btn btn-default");
        p.appendChild(cancel);
        a.appendChild(p);
        w.appendChild(a);
    }
    else {
        var w = document.getElementById('mstate_container');
        var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
        var a = document.createElement("div");
        a.setAttribute('name', val);
        a.setAttribute('id', "mealy_" + val);
        var p = document.createElement("p");
        var state_name = document.createElement("input");
        state_name.type = "text";
        state_name.placeholder = "State Name";
        state_name.name = "mstate_name" + val;
        p.appendChild(state_name);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "cancel";
        cancel.setAttribute('name',"mcancel" + val);
        cancel.setAttribute("onclick","cancel('" + cancel.name + "')");
        cancel.setAttribute("class","btn btn-default");
        p.appendChild(cancel);
        a.appendChild(p);
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
        var p = document.createElement("p");
        var state = document.createElement("input");
        state.type = "text";
        state.placeholder = "State Name";
        state.name = "state" + val;
        p.appendChild(state);
        var sp = document.createElement("span");
        sp.innerText = " to ";
        p.appendChild(sp);
        var next_state = document.createElement("input");
        next_state.type = "text";
        next_state.placeholder = "Next State";
        next_state.name = "next_state" + val;
        p.appendChild(next_state);
        var spa = document.createElement("span");
        spa.innerText = " on ";
        p.appendChild(spa);
        var input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Input Value";
        input.name = "input" + val;
        p.appendChild(input);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "cancel";
        cancel.setAttribute('name',"tcancel" + val);
        cancel.setAttribute("onclick","cancel('" + cancel.name + "')");
        cancel.setAttribute("class","btn btn-default");
        p.appendChild(cancel);
        a.appendChild(p);
        w.appendChild(a);
    }
    else {
        var w = document.getElementById('mtransition_container');
        var val = (parseInt(w.lastElementChild.getAttribute('name')) + 1).toString();
        var a = document.createElement("div");
        a.setAttribute('name', val);
        a.setAttribute('id', "tmealy_" + val);
        var p = document.createElement("p");
        var state = document.createElement("input");
        state.type = "text";
        state.placeholder = "State Name";
        state.name = "mstate" + val;
        p.appendChild(state);
        var sp = document.createElement("span");
        sp.innerText = " to ";
        p.appendChild(sp);
        var next_state = document.createElement("input");
        next_state.type = "text";
        next_state.placeholder = "Next State";
        next_state.name = "mnext_state" + val;
        p.appendChild(next_state);
        var spa = document.createElement("span");
        spa.innerText = " on ";
        p.appendChild(spa);
        var input = document.createElement("input");
        input.type = "text";
        input.placeholder = "Input Value";
        input.name = "minput" + val;
        p.appendChild(input);
        sp = document.createElement("span");
        sp.innerText = " gives ";
        p.appendChild(sp);
        var output = document.createElement("input");
        output.type = "text";
        output.placeholder = "Input Value";
        output.name = "moutput" + val;
        p.appendChild(output);
        var cancel = document.createElement("button");
        cancel.type = "button";
        cancel.innerText = "cancel";
        cancel.setAttribute('name',"tmcancel" + val);
        cancel.setAttribute("onclick","cancel('" + cancel.name + "')");
        cancel.setAttribute("class","btn btn-default");
        p.appendChild(cancel);
        a.appendChild(p);
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
    if ("cance" === argument.slice(0,5))
        a = "moore_" + argument.charAt(6);
    else if ("mcanc" === argument.slice(0,5))
        a = "mealy_" + argument.charAt(7);
    else if ("tcanc" === argument.slice(0,5))
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
    if (doc.style.display === "none"){
        doc.style.display = "block";
        doc.getElementByTagName("button").innerText = "Remove Constraints" ;
    }
    else{
        doc.style.display = "none";
        doc.getElementByTagName("button").innerText = "Add Constraints" ;
    }

}