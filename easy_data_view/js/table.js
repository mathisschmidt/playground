class InputType {
    // Text inputs
    static TEXT = new InputType('text', 'Text', 'text');
    static PASSWORD = new InputType('password', 'Password', 'text');
    static EMAIL = new InputType('email', 'Email', 'text');
    static SEARCH = new InputType('search', 'Search', 'text');
    static TEL = new InputType('tel', 'Telephone', 'text');
    static URL = new InputType('url', 'URL', 'text');

    // Number inputs
    static NUMBER = new InputType('number', 'Number', 'number');
    static RANGE = new InputType('range', 'Range', 'number');

    // Date/Time inputs
    static DATE = new InputType('date', 'Date', 'date');
    static DATETIME_LOCAL = new InputType('datetime-local', 'Date & Time', 'date');
    static TIME = new InputType('time', 'Time', 'date');
    static WEEK = new InputType('week', 'Week', 'date');
    static MONTH = new InputType('month', 'Month', 'date');

    // Selection inputs
    static SELECT = new InputType('select', 'Select', 'selection');
    static CHECKBOX = new InputType('checkbox', 'Checkbox', 'selection');
    static RADIO = new InputType('radio', 'Radio', 'selection');

    // File input
    static FILE = new InputType('file', 'File', 'file');

    // Color picker
    static COLOR = new InputType('color', 'Color', 'color');

    // Buttons
    static BUTTON = new InputType('button', 'Button', 'button');
    static SUBMIT = new InputType('submit', 'Submit', 'button');
    static RESET = new InputType('reset', 'Reset', 'button');
    static IMAGE = new InputType('image', 'Image', 'button');

    // Hidden
    static HIDDEN = new InputType('hidden', 'Hidden', 'hidden');

    constructor(value, label, category) {
        this.value = value;
        this.label = label;
        this.category = category;
    }

    isTextType() {
        return this.category === 'text';
    }

    isNumberType() {
        return this.category === 'number';
    }

    isSelectType() {
        return this.value === InputType.SELECT.value;
    }

    static values() {
        return [
            InputType.TEXT, InputType.PASSWORD, InputType.EMAIL, InputType.SEARCH,
            InputType.TEL, InputType.URL, InputType.NUMBER, InputType.RANGE,
            InputType.DATE, InputType.DATETIME_LOCAL, InputType.TIME,
            InputType.WEEK, InputType.MONTH, InputType.CHECKBOX, InputType.RADIO,
            InputType.FILE, InputType.COLOR, InputType.BUTTON, InputType.SUBMIT,
            InputType.RESET, InputType.IMAGE, InputType.HIDDEN
        ];
    }

    static fromJson(json) {
        return new InputType(
            json.value,
            json.label,
            json.category
        );
    }
}

class ColumnInfo {
    constructor(
        name,
        label,
        type = InputType.TEXT,
        sortable = false,
        searchable = false,
        showInTable = true,
        options = [],
        autoIncrement = false
    ) {
        this.name = name;
        this.label = label;
        this.type = type;
        this.sortable = sortable;
        this.searchable = searchable;
        this.showInTable = showInTable;
        this.options = options;
        this.autoIncrement = autoIncrement;
    }

    static fromJson(json) {
        return new ColumnInfo(
            json.name,
            json.label,
            InputType.fromJson(json.type),
            json.sortable,
            json.searchable,
            json.showInTable,
            json.options,
            json.autoIncrement
        );
    }
}

// Service that saves/loads table definitions + data to localStorage.
class TableStorageService {
    static save(tableInfos, id) {
        if (id === undefined) {
            console.log('TableStorageService.save called without id');
            return false
        }
        try {
            localStorage.setItem(id, JSON.stringify(tableInfos));
            return true;
        } catch (e) {
            console.warn('Failed to save table to localStorage', e);
            return false;
        }
    }

    static load(id) {
        const raw = localStorage.getItem(id);
        if (!raw) {
            throw new Error(`No saved table with id ${id} found in localStorage`);
        }
        try {
            return TableInfos.fromJson(JSON.parse(raw));
        }catch (e) {
            throw new Error(`Failed to parse stored table with id ${id}: ${e.message}`);
        }
    }
}

/*TODO: add a checker for check that a columns is a type ColumnInfo*/
/*TODO: find a way to manage the ID (all data will always have ID so we can make a global solution)*/
class TableInfos {
    constructor(id, columns = [], data = []) {
        this.id = id
        this.columns = columns;
        this.data = data;
        // Keep columns ordered by name so UI (form, headers, rows) stays consistent
        this.sortColumns();
        this.validateDataStructure(false);
    }

    // Sort columns alphabetically by name
    sortColumns() {
        this.columns.sort((a, b) => a.name.localeCompare(b.name));
    }

    persist() {
        try {
            let res = TableStorageService.save(this, this.id);
            if (!res) throw new Error('Save operation failed');
        } catch (e) {
            // TODO: add a notification
            console.warn('Failed to persist table infos', e);
        }
    }

    get columnNames() {
        return this.columns.map(col => col.name);
    }

    columnHaveToBeShow(colName) {
        const col = this.columns.find(c => c.name === colName);
        return col ? col.showInTable : false;
    }

    validateDataStructure(applyAutoIncrement = true) {
        if (this.data.length === 0) return;
        this.data.forEach(row =>
            this.validateRow(row, applyAutoIncrement)
        );
    }

    validateRow(row, applyAutoIncrement = true) {
        // TODO: check row is a dictionary
        // TODO: Maybe this logic can be in the columns class
        Object.entries(row).forEach(([key, value]) => {
            let columnDef = this.columns.find(col => col.name === key);

            if (!columnDef) {
                throw new Error(`Column ${key} does not exist in column definitions`);
            }

            if (applyAutoIncrement && columnDef.autoIncrement) {
                let maxId = this.data.reduce((max, r) => r[key] > max ? r[key] : max, 0);
                row[key] = maxId + 1;
            }
        });

        let notFoundKeys = this.columnNames.filter(colName => !Object.keys(row).includes(colName));
        if (notFoundKeys.length > 0) {
            throw new Error(`Row is missing keys: ${notFoundKeys}`);
        }
    }

    initNewItem() {
        let newItem = {};
        this.columns.forEach(col => {
            newItem[col.name] = null;
        });
        return newItem;
    }

    addRow(row) {
        this.validateRow(row)
        this.data.push(row);
        this.persist();
    }

    removeRow(item) {
        const index = this.data.findIndex(item =>
            Object.entries(item).every(([key, value]) => item[key] === value)
        );

        if (index !== -1) {
            this.data.splice(index, 1);
            this.persist();
        } else {
            throw new Error(`Row not found in data`);
        }
    }

    updateRow(index, newRow) {
        // TODO: be done later
    }

    addColumn(column, defaultValue = null) {
        if (!this.columnNames.includes(column.name)) {
            this.columns.push(column);
            // keep the column list sorted after adding
            this.sortColumns();
            this.data.forEach(row => {
                row[column.name] = defaultValue;
            });
            this.persist();
        } else {
            throw new Error('Column with this name already exists');
        }
    }

    static fromJson(json) {
        const columns = json.columns.map(colJson => ColumnInfo.fromJson(colJson));
        return new TableInfos(
            json.id,
            columns,
            json.data
        );
    }
}

export function table() {
    let id = 'easy_data_view_table_data_1';
    let tableInfos = null;

    try {
        tableInfos = TableStorageService.load(id);
    } catch (e) {
        console.warn('No saved table found, initializing new table.', e);
    }

    if (!tableInfos) {
        tableInfos = new TableInfos(id, [
                new ColumnInfo('id', 'ID', InputType.NUMBER, true, true, true, [], true),
                new ColumnInfo('user', 'User', InputType.TEXT, true, true),
                new ColumnInfo('status', 'Status', InputType.SELECT, true, true, true, [
                    { value: 'active', label: 'Active' },
                    { value: 'pending', label: 'Pending' },
                    { value: 'inactive', label: 'Inactive' }
                ]),
                new ColumnInfo('amount', 'Amount', InputType.NUMBER, true, false)
            ],
            [
                { id: 1, user: 'John Doe', status: 'active', amount: 2450 },
                { id: 2, user: 'Sarah Smith', status: 'active', amount: 1890 },
                { id: 3, user: 'Mike Johnson', status: 'pending', amount: 3200 },
                { id: 4, user: 'Emily Brown', status: 'active', amount: 4120 },
                { id: 5, user: 'David Lee', status: 'inactive', amount: 890 }
            ]
        );
    }

    return {
        newItem: {},
        tableInfos: tableInfos,
        addRow() {
            this.tableInfos.addRow(this.newItem);
            this.newItem = this.tableInfos.initNewItem();
        },
        init() {
            this.newItem = this.tableInfos.initNewItem();
        }
    }
}