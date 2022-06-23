let jsConfig = {
    'useColors': undefined,
    'updateEditFieldsUrl': '',
    'updateCollapseSettingUrl': '',
    'addTransactionUrl': '',
    'newGroupInputAdded': false,
    'expenseGroupOptions': {},
    'incomeGroupOptions': {}
};

jsConfig.init = function() {
    if (jsConfig.useColors) {
        jsConfig.colorElements();
    }

    jsConfig.expandCollapseTransactions();
    jsConfig.addEditFieldClickEvent();
    jsConfig.addTransactionClickEvent();
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

// Expand/Collapse for the Transaction lists
jsConfig.expandCollapseTransactions = function() {
    let transactionsToggle = document.querySelector('.transactions-toggle');
    let transactionsBody = document.querySelector('.transactions-body');

    transactionsToggle.addEventListener('click', function(e) {
        let params = {
            'collapse': undefined
        };

        if (hasClass(transactionsBody, 'hidden')) {
            params.collapse = 0;
            removeClass(transactionsBody, 'hidden');
            transactionsToggle.innerHTML = 'Collapse';
        } else {
            params.collapse = 1;
            addClass(transactionsBody, 'hidden');
            transactionsToggle.innerHTML = 'Expand';
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
            <input class="edit-field-value" name="new-value" type="${editField.dataset.type}" placeholder="${currentValue}">
            <button class="edit-field-submit">Submit</button>
        </div>
    `;
    document.body.appendChild(formTemplateDiv);
    formTemplateDiv.querySelector('input').focus();
};

// Form submit event
jsConfig.editFormSubmitEvent = function(editField) {
    document.querySelector('.edit-field-submit').addEventListener('click', function() {
        let params = {
            'model': editField.dataset.model,
            'id': editField.dataset.id,
            'field': editField.dataset.field,
            'newValue': document.querySelector('.edit-field-value').value,
            'fieldValue': editField.dataset.fieldValue
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

// Add transaction functionality
jsConfig.addTransactionClickEvent = function () {
    document.querySelectorAll('.add-transaction-btn').forEach(function (item) {
        item.addEventListener('click', function (e) {
            let addTransactionBtn = e.target;
            let transactionType = e.target.dataset.type;

            if (hasClass(addTransactionBtn, 'active')) {
                jsConfig.addTransactionFormTeardown();
                return;
            }

            jsConfig.addTransactionFormTeardown();

            addClass(addTransactionBtn, 'active');
            jsConfig.appendAddTransactionForm(addTransactionBtn, transactionType);
        });
    });
};

// Create/append form to add transaction / group
jsConfig.appendAddTransactionForm = function(addTransactionBtn, transactionType) {
    let top = `${addTransactionBtn.offsetTop + addTransactionBtn.offsetHeight}px`;
    let left = `${addTransactionBtn.offsetLeft}px`;
    let styleString = `style="top: ${top}; left: ${left};"`;
    let transactionTypeDisplay = jsConfig.getTransactionTypeDisplay(transactionType);
    let groupOptions = transactionType == 'ex' ? jsConfig.expenseGroupOptions : jsConfig.incomeGroupOptions;
    let formTemplateDiv = jsConfig.getNewDivElement(`
        <form action="${jsConfig.addTransactionUrl}" method="post" class="add-transaction-form" ${styleString}>
            ${jsConfig.getAddTransactionFormRow({
                'name': 'transaction-group-name',
                'label': `${transactionTypeDisplay} Group`,
                'selectOptions': groupOptions
            })}

            ${jsConfig.getAddTransactionFormRow({
                'name': 'new-transaction-type',
                'type': 'text',
                'value': transactionType,
                'hidden': true
            })}

            ${jsConfig.getAddTransactionFormRow({
                'name': 'new-transaction-name',
                'label': `${transactionTypeDisplay} Name`,
                'type': 'text',
                'placeholder': 'ex. pizza'
            })}

            ${jsConfig.getAddTransactionFormRow({
                'name': 'new-transaction-amount',
                'label': `${transactionTypeDisplay} Amount`,
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
    formTemplateDiv.querySelector('input[name="new-transaction-name"]').focus();

    jsConfig.addNewGroupClickEvent(formTemplateDiv, transactionType);
};

jsConfig.addNewGroupClickEvent = function(formTemplateDiv, transactionType) {
    let groupSelect = formTemplateDiv.querySelector('select');
    let inputName = 'transaction-group-name';

    groupSelect.addEventListener('change', function() {
        if (this.value === 'add' && !jsConfig.newGroupInputAdded) {
            let groupNameDiv = jsConfig.getNewDivElement(`
                ${jsConfig.getAddTransactionFormRow({
                    'name': 'transaction-group-type',
                    'type': 'text',
                    'value': transactionType,
                    'hidden': true
                })}

                ${jsConfig.getAddTransactionFormRow({
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

jsConfig.getAddTransactionFormRow = function(inputAttrs) {
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
            class="${inputAttrs.hidden ? 'hidden' : ''}"
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
            <label class="${inputAttrs.hidden ? 'hidden' : ''}" for="${inputAttrs.name}">${inputAttrs.label}</label>
            ${selectHtml ? selectHtml : ''}
            ${inputHtml ? inputHtml : ''}
        </div>
    `;
};

jsConfig.addTransactionFormTeardown = function() {
    let addTransactionForms = document.querySelectorAll('.add-transaction-form');
    addTransactionForms.forEach(function(form) {
       form.remove();
    });

    let addTransactionBtns = document.querySelectorAll('.add-transaction-btn');
    addTransactionBtns.forEach(function(btn) {
      removeClass(btn, 'active');
    });

    jsConfig.newGroupInputAdded = false;
};

jsConfig.getTransactionTypeDisplay = function(transactionType) {
    return transactionType === 'in' ? 'Income' : 'Expense';
};