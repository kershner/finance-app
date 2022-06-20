let jsConfig = {
    'updateEditFieldsUrl': ''
};

jsConfig.init = function() {
    //jsConfig.colorElements();
    jsConfig.expandCollapseExpenses();
    jsConfig.addEditFieldClickEvent();
};

jsConfig.colorElements = function() {
    let randomColorElements = [
        ...document.querySelectorAll('.value-with-label p:first-of-type'),
        ...document.querySelectorAll('.component-title'),
        //...document.querySelectorAll('.expense-group-title'),
        ...document.querySelectorAll('th')
    ];

    randomColorElements.forEach(element => {
        element.style.color = randomColor({
            'luminosity': 'bright'
        });
    })
};

// Expand/Collapse for the Expenses list
jsConfig.expandCollapseExpenses = function() {
    let expensesToggle = document.querySelectorAll('.expenses-toggle')[0];
    let expensesList = document.querySelectorAll('.expenses-list')[0];

    expensesToggle.addEventListener('click', function(e) {
        if (hasClass(expensesList, 'hidden')) {
            removeClass(expensesList, 'hidden');
            expensesToggle.innerHTML = 'Collapse';
        } else {
            addClass(expensesList, 'hidden');
            expensesToggle.innerHTML = 'Expand';
        }
    });
};

jsConfig.addEditFieldClickEvent = function() {
    document.querySelectorAll('.edit-field').forEach(function(e) {
        e.addEventListener('click', function(e) {
            jsConfig.editFieldClickEvent(e.target);
        });
    });
};

jsConfig.editFieldClickEvent = function(editField) {
    if (hasClass(editField, 'edit-field-active')) {
        jsConfig.editFormTeardown();
        return;
    }

    jsConfig.editFormTeardown();
    addClass(editField, 'edit-field-active');

    // Create/append form to edit the value
    let top = `${editField.offsetTop + editField.offsetHeight}px`;
    let left = `${editField.offsetLeft}px`;
    let styleString = `style="top: ${top}; left: ${left};"`;
    let formTemplateDiv = document.createElement('div');
    let currentValue = editField.dataset.currentValue;
    if (editField.dataset.type === 'number') {
        currentValue = Number(currentValue.replace(/[^0-9\.]+/g,""));
    }

    formTemplateDiv.innerHTML = `
        <div class="edit-field-form" ${styleString}>
            <label for="new-value">${editField.dataset.label}</label>
            <input class="edit-field-value" name="new-value" type="${editField.dataset.type}" value="${currentValue}">
            <button class="edit-field-submit">Submit</button>
        </div>
    `;
    document.body.appendChild(formTemplateDiv);

    // Form submit event
    document.querySelector('.edit-field-submit').addEventListener('click', function() {
        let params = {
            'model': editField.dataset.model,
            'field': editField.dataset.field,
            'fieldValue': editField.dataset.fieldValue,
            'id': editField.dataset.id,
            'newValue': document.querySelector('.edit-field-value').value
        };
        fetchWrapper(jsConfig.updateEditFieldsUrl, 'post', params, function(data) {
            if (data.success === true) {
                location.reload();
            }
        });
    });
};

jsConfig.editFormTeardown = function() {
    let allOpenEditForms = document.querySelectorAll('.edit-field-form');
    allOpenEditForms.forEach(openEditForm => {
       openEditForm.remove();
    });

    let allEditFields = document.querySelectorAll('.edit-field');
    allEditFields.forEach(editField => {
       removeClass(editField, 'edit-field-active');
    });
};
