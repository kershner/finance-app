let jsConfig = {
    'useColors': undefined,
    'updateEditFieldsUrl': '',
    'updateCollapseSettingUrl': '',
    'addExpenseUrl': '',
    'newGroupInputAdded': false,
    'groupOptions': {}
};

jsConfig.init = function() {
    if (jsConfig.useColors) {
        jsConfig.colorElements();
    }

    jsConfig.expandCollapseExpenses();
    jsConfig.addEditFieldClickEvent();
    jsConfig.addExpenseClickEvent();
};

jsConfig.colorElements = function() {
    let randomTextColorElements = [
        ...document.querySelectorAll('.value-with-label p:first-of-type'),
        ...document.querySelectorAll('.expense-group-title'),
        ...document.querySelectorAll('th')
    ];
    let randomBackgroundColorElements = [
        ...document.querySelectorAll('.component-title')
    ];

    randomTextColorElements.forEach(element => {
        element.style.color = randomColor({
            'luminosity': 'bright'
        });
    });
    randomBackgroundColorElements.forEach(element => {
        element.style.backgroundColor = randomColor({
            'luminosity': 'bright'
        });
    });
};

// Expand/Collapse for the Expenses list
jsConfig.expandCollapseExpenses = function() {
    let expensesToggle = document.querySelectorAll('.expenses-toggle')[0];
    let expensesList = document.querySelectorAll('.expenses-list')[0];

    expensesToggle.addEventListener('click', function(e) {
        let params = {
            'collapse': undefined
        };

        if (hasClass(expensesList, 'hidden')) {
            params.collapse = 0;
            removeClass(expensesList, 'hidden');
            expensesToggle.innerHTML = 'Collapse';
        } else {
            params.collapse = 1;
            addClass(expensesList, 'hidden');
            expensesToggle.innerHTML = 'Expand';
        }

        // Async fetch call to update user model setting
        fetchWrapper(jsConfig.updateCollapseSettingUrl, 'post', params, function(data) {
            console.log(data);
        });
    });
};

// Edit field menu
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

    jsConfig.addEditFieldForm(editField);
    jsConfig.editFormSubmitEvent(editField);
};

// Create/append form to edit the value
jsConfig.addEditFieldForm = function(editField) {
    let top = `${editField.offsetTop + editField.offsetHeight}px`;
    let left = `${editField.offsetLeft}px`;
    let styleString = `style="top: ${top}; left: ${left};"`;
    let formTemplateDiv = document.createElement('div');
    let currentValue = editField.dataset.currentValue;
    if (editField.dataset.type === 'decimal') {
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
};

// Form submit event
jsConfig.editFormSubmitEvent = function(editField) {
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

// Add expense functionality
jsConfig.addExpenseClickEvent = function() {
    document.querySelector('#add-expense-btn').addEventListener('click', function(e) {
        let addExpenseBtn = e.target;

        if (hasClass(addExpenseBtn, 'active')) {
            jsConfig.addExpenseFormTeardown();
            return;
        }

        addClass(addExpenseBtn, 'active');
        jsConfig.appendAddExpenseForm(addExpenseBtn);
    });
};

// Create/append form to add expense / group
jsConfig.appendAddExpenseForm = function(addExpenseBtn) {
    let top = `${addExpenseBtn.offsetTop + addExpenseBtn.offsetHeight}px`;
    let left = `${addExpenseBtn.offsetLeft}px`;
    let styleString = `style="top: ${top}; left: ${left};"`;
    let formTemplateDiv = jsConfig.getNewDivElement(`
        <form action="${jsConfig.addExpenseUrl}" method="post" class="add-expense-form" ${styleString}>
            ${jsConfig.getAddExpenseFormRow({
                'name': 'expense-group-name',
                'label': 'Group',
                'selectOptions': jsConfig.groupOptions
            })}

            ${jsConfig.getAddExpenseFormRow({
                'name': 'new-expense-name',
                'label': 'Expense Name',
                'type': 'text',
                'placeholder': 'ex. pizza'
            })}

            ${jsConfig.getAddExpenseFormRow({
                'name': 'new-expense-amount',
                'label': 'Expense Amount',
                'type': 'decimal',
                'placeholder': '0.0',
                'min': 1,
                'value': 0.0
            })}

            <div class="form-row">
                <button type="submit">Add</button>
            </div>
        </form>
    `);
    document.body.appendChild(formTemplateDiv);

    jsConfig.addNewGroupClickEvent(formTemplateDiv);
};

jsConfig.addNewGroupClickEvent = function(formTemplateDiv) {
    let groupSelect = formTemplateDiv.querySelector('select');
    let inputName = 'expense-group-name';

    groupSelect.addEventListener('change', function() {
        if (this.value === 'add' && !jsConfig.newGroupInputAdded) {
            let groupNameDiv = jsConfig.getNewDivElement(`
                ${jsConfig.getAddExpenseFormRow({
                    'name': inputName,
                    'label': 'New Group Name',
                    'type': 'text',
                    'placeholder': 'ex. Video Games'
                })}
            `);
            groupSelect.parentNode.insertBefore(groupNameDiv, groupSelect.nextSibling);
            jsConfig.newGroupInputAdded = true;
        } else {
            let newGroupInput = document.querySelector(`input[name=${inputName}]`);
            if (newGroupInput !== null) {
                document.querySelector(`input[name=${inputName}]`).parentNode.remove();
                jsConfig.newGroupInputAdded = false;
            }
        }
    });
};

jsConfig.getNewDivElement = function(innerHtml) {
    let newDivElement = document.createElement('div');
    newDivElement.innerHTML = innerHtml;
    return newDivElement
};

jsConfig.getAddExpenseFormRow = function(inputAttrs) {
    let selectHtml = undefined;
    let inputHtml = undefined;

    if (inputAttrs.selectOptions !== undefined) {
        let selectOptionsHtml = '';
        for (let option in inputAttrs.selectOptions) {
            selectOptionsHtml += `<option value="${option}">${inputAttrs.selectOptions[option]}</option>`;
        }
        selectHtml = `<select name="${inputAttrs.name}" required>${selectOptionsHtml}</select>`;
    } else {
        inputHtml = `
            <input
            name="${inputAttrs.name}"
            type="${inputAttrs.type}"
            placeholder="${inputAttrs.placeholder ? inputAttrs.placeholder : ''}"
            min="${inputAttrs.min ? inputAttrs.min : 0}"
            value="${inputAttrs.value ? inputAttrs.value : ''}"
            required>
        `;
    }

    return `
        <div class="form-row">
            <label for="${inputAttrs.name}">${inputAttrs.label}</label>
            ${selectHtml ? selectHtml : ''}
            ${inputHtml ? inputHtml : ''}
        </div>
    `;
};

jsConfig.addExpenseFormTeardown = function() {
    let addExpenseForm = document.querySelector('.add-expense-form');
    addExpenseForm.remove();

    let addExpenseBtn = document.querySelector('#add-expense-btn');
    removeClass(addExpenseBtn, 'active');

    jsConfig.newGroupInputAdded = false;
};