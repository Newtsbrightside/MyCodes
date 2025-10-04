document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const taskInput = document.getElementById('taskInput');
    const dateInput = document.getElementById('dateInput');
    const addBtn = document.getElementById('addBtn');
    const searchInput = document.getElementById('searchInput');
    const taskList = document.getElementById('taskList');
    const noTasks = document.getElementById('noTasks');
    const totalTasks = document.getElementById('total-tasks');
    const completedTasks = document.getElementById('completed-tasks');
    const pendingTasks = document.getElementById('pending-tasks');
    const progress = document.getElementById('progress');
    const progressBar = document.getElementById('progress-bar');
    const sortBtn = document.getElementById('sortBtn');
    const deleteAllBtn = document.getElementById('deleteAllBtn');
    const filterBtn = document.getElementById('filterBtn');
    
    // Set today's date as default
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    dateInput.value = formattedDate;

    // Theme options
    const themes = [
        { name: 'Light', bgColor: '#ffffff', textColor: '#333333', accent: '#2196f3', taskBg: '#ffffff', themeSelectorText: '#333333' },
        { name: 'Dark', bgColor: '#1a1a2e', textColor: '#ffffff', accent: '#ff6b6b', taskBg: '#232342', themeSelectorText: '#333333' },
        { name: 'Purple', bgColor: '#2b124c', textColor: '#ffffff', accent: '#7b2cbf', taskBg: '#3b1a69', themeSelectorText: '#333333' },
        { name: 'Green', bgColor: '#1b4332', textColor: '#ffffff', accent: '#52b788', taskBg: '#2d5a46', themeSelectorText: '#333333' }
    ];
    
    // Current theme (default to light)
    let currentTheme = localStorage.getItem('theme') ? 
        JSON.parse(localStorage.getItem('theme')) : themes[0];
    
    // Current filter ('all', 'pending', 'completed')
    let currentFilter = 'all';

    // Priority options
    const priorities = [
        { name: 'High', color: '#f44336' },
        { name: 'Medium', color: '#ff9800' },
        { name: 'Low', color: '#4caf50' },
        { name: 'None', color: '#9e9e9e' }
    ];

    // Load tasks from local storage
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

    // Create theme button
    createThemeButton();
    applyTheme(currentTheme);

    // Function to save tasks to local storage
    function saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
        updateStats();
    }

    // Update statistics and progress
    function updateStats() {
        const total = tasks.length;
        let completed = 0;
        let totalItems = 0;
        
        tasks.forEach(task => {
            totalItems++;
            if (task.completed) completed++;
            
            if (task.subtasks && task.subtasks.length > 0) {
                totalItems += task.subtasks.length;
                completed += task.subtasks.filter(subtask => subtask.completed).length;
            }
        });
        
        const pending = totalItems - completed;
        const progressPercentage = totalItems === 0 ? 0 : Math.round((completed / totalItems) * 100);

        totalTasks.textContent = total;
        completedTasks.textContent = completed;
        pendingTasks.textContent = pending;
        progress.textContent = `${progressPercentage}%`;
        
        // Update progress bar
        progressBar.style.width = `${progressPercentage}%`;
        
        // Show or hide no tasks message
        if (total === 0) {
            noTasks.style.display = 'block';
        } else {
            noTasks.style.display = 'none';
        }
    }

    // Format date to display
    function formatDate(dateString) {
        if (!dateString) return 'No due date';
        
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric',
            year: 'numeric'
        });
    }

    // Add a new task
    function addTask() {
        const text = taskInput.value.trim();
        const date = dateInput.value;
        
        if (text) {
            tasks.push({
                text,
                date,
                completed: false,
                priority: priorities[3], // Default to 'None' priority
                subtasks: []
            });
            
            saveTasks();
            applyFilter();
            taskInput.value = '';
            dateInput.value = formattedDate;
        }
    }

    // Delete a task
    function deleteTask(index) {
        tasks.splice(index, 1);
        saveTasks();
        applyFilter();
    }

    // Toggle task completion
    function toggleComplete(index) {
        tasks[index].completed = !tasks[index].completed;
        
        // If task is marked as complete, also complete all subtasks
        if (tasks[index].completed && tasks[index].subtasks && tasks[index].subtasks.length > 0) {
            tasks[index].subtasks.forEach(subtask => {
                subtask.completed = true;
            });
        }
        
        saveTasks();
        applyFilter();
    }

    // Toggle subtask completion
    function toggleSubtaskComplete(taskIndex, subtaskIndex) {
        tasks[taskIndex].subtasks[subtaskIndex].completed = !tasks[taskIndex].subtasks[subtaskIndex].completed;
        saveTasks();
        applyFilter();
    }

    // Delete a subtask
    function deleteSubtask(taskIndex, subtaskIndex) {
        tasks[taskIndex].subtasks.splice(subtaskIndex, 1);
        saveTasks();
        applyFilter();
    }

    // Add a subtask to a task
    function addSubtask(index) {
        const subtaskText = prompt('Enter subtask:');
        if (subtaskText && subtaskText.trim()) {
            if (!tasks[index].subtasks) {
                tasks[index].subtasks = [];
            }
            
            tasks[index].subtasks.push({
                text: subtaskText.trim(),
                completed: false
            });
            
            saveTasks();
            applyFilter();
        }
    }

    // Set priority for a task
    function setPriority(taskIndex, priority) {
        tasks[taskIndex].priority = priority;
        saveTasks();
        applyFilter();
    }

    // Search tasks
    function searchTasks(query) {
        if (!query) {
            applyFilter();
            return;
        }
        
        query = query.toLowerCase();
        const filteredTasks = tasks.filter(task => 
            task.text.toLowerCase().includes(query)
        );
        renderTasks(filteredTasks);
    }

    // Sort tasks by date
    let sortOrder = 'asc';
    function sortTasksByDate() {
        sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
        
        tasks.sort((a, b) => {
            const dateA = new Date(a.date);
            const dateB = new Date(b.date);
            return sortOrder === 'asc' ? dateA - dateB : dateB - dateA;
        });
        
        saveTasks();
        applyFilter();
    }

    // Delete all tasks
    function deleteAllTasks() {
        if (tasks.length > 0 && confirm('Are you sure you want to delete all tasks?')) {
            tasks = [];
            saveTasks();
            applyFilter();
        }
    }

    // Apply current filter
    function applyFilter() {
        let filteredTasks;
        
        if (currentFilter === 'all') {
            // Show all tasks
            filteredTasks = tasks;
        } else if (currentFilter === 'pending') {
            // Filter by pending status
            filteredTasks = tasks.filter(task => !task.completed);
        } else if (currentFilter === 'completed') {
            // Filter by completed status
            filteredTasks = tasks.filter(task => task.completed);
        } else if (currentFilter.startsWith('priority-')) {
            // Filter by priority
            const priorityName = currentFilter.replace('priority-', '');
            filteredTasks = tasks.filter(task => 
                task.priority && 
                task.priority.name.toLowerCase() === priorityName
            );
        }
        
        renderTasks(filteredTasks);
    }

    // Set filter
    function setFilter(filter) {
        currentFilter = filter;
        applyFilter();
    }

    // Render tasks list
    function renderTasks(tasksToRender) {
        // Clear all existing tasks except the "no tasks" message
        const existingTasks = taskList.querySelectorAll('.task-item, .subtask-container');
        existingTasks.forEach(item => item.remove());
        
        if (tasksToRender.length === 0) {
            noTasks.style.display = 'block';
            return;
        }
        
        noTasks.style.display = 'none';
        
        // Render each task
        tasksToRender.forEach((task, index) => {
            const actualIndex = tasks.indexOf(task); // Get the actual index from the full tasks array
            
            // Create task item
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';
            taskItem.dataset.index = actualIndex;
            taskItem.style.backgroundColor = currentTheme.taskBg;
            taskItem.style.position = 'relative';
            taskItem.style.zIndex = '1';
            
            // Task content (left side)
            const taskContent = document.createElement('div');
            taskContent.style.width = '30%';
            taskContent.style.display = 'flex';
            taskContent.style.alignItems = 'center';
            
            // Priority indicator
            const priorityIndicator = document.createElement('div');
            priorityIndicator.style.display = 'flex';
            priorityIndicator.style.alignItems = 'center';
            priorityIndicator.style.marginRight = '10px';
            
            const priorityDot = document.createElement('span');
            priorityDot.style.width = '10px';
            priorityDot.style.height = '10px';
            priorityDot.style.borderRadius = '50%';
            priorityDot.style.backgroundColor = task.priority?.color || '#9e9e9e';
            priorityDot.style.marginRight = '5px';
            
            const priorityText = document.createElement('span');
            priorityText.textContent = task.priority?.name || 'None';
            priorityText.style.fontSize = '0.7rem';
            priorityText.style.color = currentTheme.textColor;
            
            priorityIndicator.appendChild(priorityDot);
            priorityIndicator.appendChild(priorityText);
            
            // Task text
            const taskText = document.createElement('span');
            taskText.textContent = task.text;
            taskText.style.textDecoration = task.completed ? 'line-through' : 'none';
            taskText.style.color = task.completed ? '#888' : currentTheme.textColor;
            
            taskContent.appendChild(priorityIndicator);
            taskContent.appendChild(taskText);
            
            // Due date (middle)
            const dueDate = document.createElement('div');
            dueDate.style.width = '30%';
            dueDate.textContent = formatDate(task.date);
            dueDate.style.color = currentTheme.textColor;
            
            // Status (right)
            const statusCol = document.createElement('div');
            statusCol.style.width = '20%';
            
            const statusBadge = document.createElement('span');
            statusBadge.style.padding = '4px 12px';
            statusBadge.style.borderRadius = '15px';
            statusBadge.style.fontSize = '0.75rem';
            
            if (task.completed) {
                statusBadge.style.backgroundColor = '#e8f5e9';
                statusBadge.style.color = '#4caf50';
                statusBadge.textContent = 'Completed';
            } else {
                statusBadge.style.backgroundColor = '#fff8e1';
                statusBadge.style.color = '#ff9800';
                statusBadge.textContent = 'Pending';
            }
            
            statusCol.appendChild(statusBadge);
            
            // Actions column
            const actionsCol = document.createElement('div');
            actionsCol.style.width = '20%';
            actionsCol.style.display = 'flex';
            actionsCol.style.justifyContent = 'flex-end';
            actionsCol.style.gap = '5px';
            
            // Priority button
            const priorityBtn = document.createElement('button');
            priorityBtn.style.width = '30px';
            priorityBtn.style.height = '30px';
            priorityBtn.style.borderRadius = '50%';
            priorityBtn.style.backgroundColor = '#9c27b0';
            priorityBtn.style.color = 'white';
            priorityBtn.style.border = 'none';
            priorityBtn.style.display = 'flex';
            priorityBtn.style.alignItems = 'center';
            priorityBtn.style.justifyContent = 'center';
            priorityBtn.style.cursor = 'pointer';
            priorityBtn.style.position = 'relative';
            priorityBtn.style.zIndex = '10';
            priorityBtn.innerHTML = `<i class="fa-solid fa-flag"></i>`;
            priorityBtn.title = 'Set Priority';
            
            priorityBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Remove any existing dropdowns first
                const existingDropdowns = document.querySelectorAll('.priority-dropdown');
                existingDropdowns.forEach(d => d.remove());
                
                // Create a visual dropdown menu
                const dropdown = document.createElement('div');
                dropdown.className = 'priority-dropdown';
                dropdown.style.display = 'block';
                dropdown.style.position = 'fixed';
                dropdown.style.backgroundColor = 'white';
                dropdown.style.border = '1px solid #ddd';
                dropdown.style.borderRadius = '5px';
                dropdown.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                dropdown.style.padding = '5px 0';
                dropdown.style.zIndex = '1000';
                dropdown.style.minWidth = '120px';
                
                // Position it properly relative to the button
                const rect = this.getBoundingClientRect();
                dropdown.style.top = (rect.bottom + window.scrollY + 5) + 'px';
                dropdown.style.left = (rect.left + window.scrollX - 50) + 'px';
                
                // Add each priority option
                priorities.forEach(priority => {
                    const option = document.createElement('div');
                    option.style.padding = '8px 15px';
                    option.style.display = 'flex';
                    option.style.alignItems = 'center';
                    option.style.cursor = 'pointer';
                    
                    // Add color dot
                    const colorDot = document.createElement('span');
                    colorDot.style.width = '12px';
                    colorDot.style.height = '12px';
                    colorDot.style.borderRadius = '50%';
                    colorDot.style.backgroundColor = priority.color;
                    colorDot.style.marginRight = '10px';
                    
                    // Add priority name
                    const name = document.createElement('span');
                    name.textContent = priority.name;
                    name.style.color = '#333';
                    
                    option.appendChild(colorDot);
                    option.appendChild(name);
                    
                    // Hover effects
                    option.addEventListener('mouseover', function() {
                        this.style.backgroundColor = '#f5f5f5';
                    });
                    
                    option.addEventListener('mouseout', function() {
                        this.style.backgroundColor = 'transparent';
                    });
                    
                    // Click handler
                    option.addEventListener('click', function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        setPriority(actualIndex, priority);
                        dropdown.remove();
                    });
                    
                    dropdown.appendChild(option);
                });
                
                // Add dropdown to the DOM
                document.body.appendChild(dropdown);
                
                // Handle clicking outside to close
                const closeDropdown = function(event) {
                    if (!dropdown.contains(event.target) && event.target !== priorityBtn) {
                        dropdown.remove();
                        document.removeEventListener('click', closeDropdown);
                    }
                };
                
                // Use setTimeout to prevent immediate closing
                setTimeout(() => {
                    document.addEventListener('click', closeDropdown);
                }, 50);
            });
            
            // Subtask button
            const subtaskBtn = document.createElement('button');
            subtaskBtn.style.width = '30px';
            subtaskBtn.style.height = '30px';
            subtaskBtn.style.borderRadius = '50%';
            subtaskBtn.style.backgroundColor = '#009688';
            subtaskBtn.style.color = 'white';
            subtaskBtn.style.border = 'none';
            subtaskBtn.style.display = 'flex';
            subtaskBtn.style.alignItems = 'center';
            subtaskBtn.style.justifyContent = 'center';
            subtaskBtn.style.cursor = 'pointer';
            subtaskBtn.style.position = 'relative';
            subtaskBtn.style.zIndex = '10';
            subtaskBtn.innerHTML = `<i class="fa-solid fa-list"></i>`;
            subtaskBtn.title = 'Add Subtask';
            
            subtaskBtn.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                addSubtask(actualIndex);
            };
            
            // Complete button
            const completeBtn = document.createElement('button');
            completeBtn.style.width = '30px';
            completeBtn.style.height = '30px';
            completeBtn.style.borderRadius = '50%';
            completeBtn.style.backgroundColor = '#4caf50';
            completeBtn.style.color = 'white';
            completeBtn.style.border = 'none';
            completeBtn.style.display = 'flex';
            completeBtn.style.alignItems = 'center';
            completeBtn.style.justifyContent = 'center';
            completeBtn.style.cursor = 'pointer';
            completeBtn.style.position = 'relative';
            completeBtn.style.zIndex = '10';
            completeBtn.innerHTML = `<i class="fa-solid fa-check"></i>`;
            completeBtn.title = 'Mark as Complete';
            
            completeBtn.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                toggleComplete(actualIndex);
            };
            
            // Delete button
            const deleteBtn = document.createElement('button');
            deleteBtn.style.width = '30px';
            deleteBtn.style.height = '30px';
            deleteBtn.style.borderRadius = '50%';
            deleteBtn.style.backgroundColor = '#f44336';
            deleteBtn.style.color = 'white';
            deleteBtn.style.border = 'none';
            deleteBtn.style.display = 'flex';
            deleteBtn.style.alignItems = 'center';
            deleteBtn.style.justifyContent = 'center';
            deleteBtn.style.cursor = 'pointer';
            deleteBtn.style.position = 'relative';
            deleteBtn.style.zIndex = '10';
            deleteBtn.innerHTML = `<i class="fa-solid fa-trash"></i>`;
            deleteBtn.title = 'Delete Task';
            
            deleteBtn.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                deleteTask(actualIndex);
            };
            
            actionsCol.appendChild(priorityBtn);
            actionsCol.appendChild(subtaskBtn);
            actionsCol.appendChild(completeBtn);
            actionsCol.appendChild(deleteBtn);
            
            // Assemble task item
            taskItem.appendChild(taskContent);
            taskItem.appendChild(dueDate);
            taskItem.appendChild(statusCol);
            taskItem.appendChild(actionsCol);
            
            taskList.appendChild(taskItem);
            
            // Render subtasks if any
            if (task.subtasks && task.subtasks.length > 0) {
                const subtasksContainer = document.createElement('div');
                subtasksContainer.className = 'subtask-container';
                subtasksContainer.style.marginLeft = '25px';
                subtasksContainer.style.borderLeft = '2px dotted #ddd';
                subtasksContainer.style.paddingLeft = '15px';
                subtasksContainer.style.marginTop = '5px';
                subtasksContainer.style.marginBottom = '10px';
                subtasksContainer.style.backgroundColor = currentTheme.taskBg;
                
                task.subtasks.forEach((subtask, subtaskIndex) => {
                    const subtaskItem = document.createElement('div');
                    subtaskItem.style.display = 'flex';
                    subtaskItem.style.alignItems = 'center';
                    subtaskItem.style.padding = '8px 0';
                    
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.checked = subtask.completed;
                    checkbox.style.marginRight = '10px';
                    checkbox.onclick = function() {
                        toggleSubtaskComplete(actualIndex, subtaskIndex);
                    };
                    
                    const subtaskText = document.createElement('span');
                    subtaskText.textContent = subtask.text;
                    subtaskText.style.flex = '1';
                    subtaskText.style.color = currentTheme.textColor;
                    subtaskText.style.textDecoration = subtask.completed ? 'line-through' : 'none';
                    
                    const deleteSubtaskBtn = document.createElement('button');
                    deleteSubtaskBtn.innerHTML = '&times;';
                    deleteSubtaskBtn.style.background = 'none';
                    deleteSubtaskBtn.style.border = 'none';
                    deleteSubtaskBtn.style.color = '#999';
                    deleteSubtaskBtn.style.fontSize = '16px';
                    deleteSubtaskBtn.style.cursor = 'pointer';
                    deleteSubtaskBtn.onclick = function() {
                        deleteSubtask(actualIndex, subtaskIndex);
                    };
                    
                    subtaskItem.appendChild(checkbox);
                    subtaskItem.appendChild(subtaskText);
                    subtaskItem.appendChild(deleteSubtaskBtn);
                    
                    subtasksContainer.appendChild(subtaskItem);
                });
                
                taskList.appendChild(subtasksContainer);
            }
        });
        
        updateStats();
    }

    // Create an action button
    function createActionButton(color, icon, title) {
        const button = document.createElement('button');
        button.style.width = '30px';
        button.style.height = '30px';
        button.style.borderRadius = '50%';
        button.style.backgroundColor = color;
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.display = 'flex';
        button.style.alignItems = 'center';
        button.style.justifyContent = 'center';
        button.style.cursor = 'pointer';
        button.style.position = 'relative';
        button.style.zIndex = '10';
        button.innerHTML = `<i class="fa-solid fa-${icon}"></i>`;
        button.title = title;
        return button;
    }

    // Show filter dropdown
    function showFilterDropdown() {
        // Remove any existing dropdowns
        const existingDropdowns = document.querySelectorAll('.priority-dropdown, .filter-dropdown, .theme-selector');
        existingDropdowns.forEach(dropdown => dropdown.remove());
        
        const dropdown = document.createElement('div');
        dropdown.className = 'filter-dropdown';
        dropdown.style.position = 'fixed';
        dropdown.style.backgroundColor = '#2b124c';
        dropdown.style.color = 'white';
        dropdown.style.borderRadius = '5px';
        dropdown.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
        dropdown.style.padding = '5px 0';
        dropdown.style.zIndex = '1000';
        dropdown.style.width = '170px'; // Slightly wider to accommodate longer text
        
        // Position the dropdown
        const rect = filterBtn.getBoundingClientRect();
        dropdown.style.top = (rect.bottom + 5) + 'px';
        dropdown.style.right = (window.innerWidth - rect.right) + 'px';
        
        // Add section title for status filters
        const statusTitle = document.createElement('div');
        statusTitle.textContent = 'Filter by Status';
        statusTitle.style.padding = '5px 15px';
        statusTitle.style.fontSize = '0.8rem';
        statusTitle.style.opacity = '0.7';
        statusTitle.style.fontWeight = 'bold';
        statusTitle.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
        dropdown.appendChild(statusTitle);
        
        // Add status filter options
        const statusFilters = [
            { name: 'All Tasks', value: 'all' },
            { name: 'Pending', value: 'pending' },
            { name: 'Completed', value: 'completed' }
        ];
        
        statusFilters.forEach(filter => {
            const option = createFilterOption(filter.name, filter.value, currentFilter);
            dropdown.appendChild(option);
        });
        
        // Add section title for priority filters
        const priorityTitle = document.createElement('div');
        priorityTitle.textContent = 'Filter by Priority';
        priorityTitle.style.padding = '5px 15px';
        priorityTitle.style.fontSize = '0.8rem';
        priorityTitle.style.opacity = '0.7';
        priorityTitle.style.fontWeight = 'bold';
        priorityTitle.style.borderTop = '1px solid rgba(255,255,255,0.2)';
        priorityTitle.style.marginTop = '5px';
        priorityTitle.style.borderBottom = '1px solid rgba(255,255,255,0.1)';
        dropdown.appendChild(priorityTitle);
        
        // Add priority filter options
        priorities.forEach(priority => {
            const option = createFilterOption(priority.name, 'priority-' + priority.name.toLowerCase(), currentFilter);
            
            // Add color dot to priority options
            const colorDot = document.createElement('span');
            colorDot.style.display = 'inline-block';
            colorDot.style.width = '8px';
            colorDot.style.height = '8px';
            colorDot.style.borderRadius = '50%';
            colorDot.style.backgroundColor = priority.color;
            colorDot.style.marginRight = '8px';
            
            option.insertBefore(colorDot, option.firstChild);
            dropdown.appendChild(option);
        });
        
        document.body.appendChild(dropdown);
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function closeDropdown(e) {
            if (!dropdown.contains(e.target) && e.target !== filterBtn) {
                dropdown.remove();
                document.removeEventListener('click', closeDropdown);
            }
        });
        
        // Helper function to create filter options
        function createFilterOption(name, value, currentFilter) {
            const option = document.createElement('div');
            option.style.padding = '8px 15px';
            option.style.cursor = 'pointer';
            option.style.display = 'flex';
            option.style.alignItems = 'center';
            
            const optionText = document.createElement('span');
            optionText.textContent = name;
            option.appendChild(optionText);
            
            if (currentFilter === value) {
                option.style.fontWeight = 'bold';
                option.style.backgroundColor = 'rgba(255,255,255,0.1)';
            }
            
            option.onmouseover = function() {
                this.style.backgroundColor = 'rgba(255,255,255,0.2)';
            };
            
            option.onmouseout = function() {
                if (currentFilter === value) {
                    this.style.backgroundColor = 'rgba(255,255,255,0.1)';
                } else {
                    this.style.backgroundColor = 'transparent';
                }
            };
            
            option.onclick = function() {
                setFilter(value);
                dropdown.remove();
            };
            
            return option;
        }
    }

    // Create theme button in top-right corner
    function createThemeButton() {
        const themeBtn = document.createElement('button');
        themeBtn.id = 'themeBtn';
        themeBtn.style.position = 'fixed';
        themeBtn.style.top = '20px';
        themeBtn.style.right = '20px';
        themeBtn.style.width = '40px';
        themeBtn.style.height = '40px';
        themeBtn.style.borderRadius = '50%';
        themeBtn.style.backgroundColor = currentTheme.accent;
        themeBtn.style.color = '#fff';
        themeBtn.style.border = 'none';
        themeBtn.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
        themeBtn.style.cursor = 'pointer';
        themeBtn.style.zIndex = '1000';
        themeBtn.style.display = 'flex';
        themeBtn.style.alignItems = 'center';
        themeBtn.style.justifyContent = 'center';
        themeBtn.innerHTML = '<i class="fa-solid fa-palette"></i>';
        themeBtn.title = 'Change Theme';
        
        themeBtn.onclick = function() {
            showThemeSelector(this);
        };
        
        document.body.appendChild(themeBtn);
    }

    // Show theme selector
    function showThemeSelector(buttonEl) {
        // Remove any existing theme selectors
        const existingDropdowns = document.querySelectorAll('.priority-dropdown, .filter-dropdown, .theme-selector');
        existingDropdowns.forEach(dropdown => dropdown.remove());
        
        const selector = document.createElement('div');
        selector.className = 'theme-selector';
        selector.style.position = 'fixed';
        selector.style.top = '70px';
        selector.style.right = '20px';
        selector.style.backgroundColor = 'white';
        selector.style.borderRadius = '8px';
        selector.style.boxShadow = '0 2px 10px rgba(0,0,0,0.2)';
        selector.style.padding = '15px';
        selector.style.zIndex = '1000';
        selector.style.width = '180px';
        
        const heading = document.createElement('h3');
        heading.textContent = 'Select Theme';
        heading.style.margin = '0 0 10px 0';
        heading.style.fontSize = '16px';
        heading.style.color = '#333'; // Always dark text for better contrast
        
        selector.appendChild(heading);
        
        themes.forEach(theme => {
            const option = document.createElement('div');
            option.style.display = 'flex';
            option.style.alignItems = 'center';
            option.style.padding = '8px 10px';
            option.style.cursor = 'pointer';
            option.style.borderRadius = '4px';
            option.style.marginBottom = '5px';
            
            if (currentTheme.name === theme.name) {
                option.style.backgroundColor = '#f0f0f0';
            }
            
            // Color preview
            const colorPreview = document.createElement('div');
            colorPreview.style.width = '24px';
            colorPreview.style.height = '24px';
            colorPreview.style.backgroundColor = theme.bgColor;
            colorPreview.style.borderRadius = '4px';
            colorPreview.style.marginRight = '10px';
            colorPreview.style.position = 'relative';
            colorPreview.style.border = '1px solid #ddd';
            
            // Accent dot
            const accentDot = document.createElement('div');
            accentDot.style.position = 'absolute';
            accentDot.style.bottom = '2px';
            accentDot.style.right = '2px';
            accentDot.style.width = '8px';
            accentDot.style.height = '8px';
            accentDot.style.borderRadius = '50%';
            accentDot.style.backgroundColor = theme.accent;
            
            colorPreview.appendChild(accentDot);
            
            const themeName = document.createElement('span');
            themeName.textContent = theme.name;
            themeName.style.color = theme.themeSelectorText; // Use theme-specific text color
            
            option.appendChild(colorPreview);
            option.appendChild(themeName);
            
            option.onmouseover = function() {
                if (currentTheme.name !== theme.name) {
                    this.style.backgroundColor = '#f8f8f8';
                }
            };
            
            option.onmouseout = function() {
                if (currentTheme.name !== theme.name) {
                    this.style.backgroundColor = 'transparent';
                }
            };
            
            option.onclick = function(e) {
                e.stopPropagation();
                currentTheme = theme;
                localStorage.setItem('theme', JSON.stringify(theme));
                applyTheme(theme);
                buttonEl.style.backgroundColor = theme.accent;
                selector.remove();
                applyFilter();
            };
            
            selector.appendChild(option);
        });
        
        document.body.appendChild(selector);
        
        // Close when clicking outside
        setTimeout(() => {
            document.addEventListener('click', function closeSelector(e) {
                if (!selector.contains(e.target) && e.target !== buttonEl) {
                    selector.remove();
                    document.removeEventListener('click', closeSelector);
                }
            });
        }, 10);
    }

    // Apply theme to document
    function applyTheme(theme) {
        document.body.style.backgroundColor = theme.bgColor;
        document.body.style.color = theme.textColor;
        
        const container = document.querySelector('.container');
        if (container) {
            container.style.backgroundColor = adjustBrightness(theme.bgColor, 10);
            container.style.boxShadow = `0 5px 15px ${adjustBrightness(theme.bgColor, -15)}`;
        }
        
        // Update task items background
        const taskItems = document.querySelectorAll('.task-item');
        taskItems.forEach(item => {
            item.style.backgroundColor = theme.taskBg;
        });
        
        // Update subtask containers background
        const subtaskContainers = document.querySelectorAll('.subtask-container');
        subtaskContainers.forEach(container => {
            container.style.backgroundColor = theme.taskBg;
        });
        
        // Update progress bar color
        if (progressBar) {
            progressBar.style.backgroundColor = theme.accent;
        }
        
        // Update add button color
        if (addBtn) {
            addBtn.style.backgroundColor = theme.accent;
        }
        
        // Update theme button if it exists
        const themeBtn = document.getElementById('themeBtn');
        if (themeBtn) {
            themeBtn.style.backgroundColor = theme.accent;
        }
        
        // Apply theme to inputs
        const inputs = document.querySelectorAll('input');
        inputs.forEach(input => {
            input.style.backgroundColor = adjustBrightness(theme.bgColor, 5);
            input.style.color = theme.textColor;
            input.style.borderColor = adjustBrightness(theme.bgColor, 15);
        });
        
        // Apply theme to buttons
        const filterBtnEl = document.getElementById('filterBtn');
        if (filterBtnEl) {
            filterBtnEl.style.backgroundColor = adjustBrightness(theme.bgColor, 5);
            filterBtnEl.style.color = theme.textColor;
            filterBtnEl.style.borderColor = adjustBrightness(theme.bgColor, 15);
        }
        
        // Override the table header background color
        const tableHeaders = document.querySelectorAll('.table-header');
        tableHeaders.forEach(header => {
            header.style.backgroundColor = adjustBrightness(theme.bgColor, 5);
            header.style.color = theme.textColor;
        });
        
        // Make sure the column headers are visible
        const columnHeaders = document.querySelectorAll('.sort-btn, .column, .task, .due-date, .status, .actions');
        columnHeaders.forEach(column => {
            column.style.color = theme.textColor;
        });
        
        // Keep delete all button red for visibility
        const deleteAllBtn = document.querySelector('.delete-all-btn');
        if (deleteAllBtn) {
            deleteAllBtn.style.backgroundColor = '#ff6b6b';
            deleteAllBtn.style.color = 'white';
        }
    }
    
    // Helper function to adjust color brightness
    function adjustBrightness(color, percent) {
        let R = parseInt(color.substring(1,3), 16);
        let G = parseInt(color.substring(3,5), 16);
        let B = parseInt(color.substring(5,7), 16);

        R = parseInt(R * (100 + percent) / 100);
        G = parseInt(G * (100 + percent) / 100);
        B = parseInt(B * (100 + percent) / 100);

        R = (R < 255) ? R : 255;  
        G = (G < 255) ? G : 255;  
        B = (B < 255) ? B : 255;  

        R = Math.max(0, R);
        G = Math.max(0, G);
        B = Math.max(0, B);

        const RR = ((R.toString(16).length === 1) ? "0" + R.toString(16) : R.toString(16));
        const GG = ((G.toString(16).length === 1) ? "0" + G.toString(16) : G.toString(16));
        const BB = ((B.toString(16).length === 1) ? "0" + B.toString(16) : B.toString(16));

        return "#"+RR+GG+BB;
    }

    // Event listeners
    addBtn.addEventListener('click', addTask);
    
    taskInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTask();
        }
    });
    
    searchInput.addEventListener('input', function() {
        searchTasks(this.value);
    });
    
    sortBtn.addEventListener('click', sortTasksByDate);
    deleteAllBtn.addEventListener('click', deleteAllTasks);
    filterBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        showFilterDropdown();
    });

    // Initial render
    applyFilter();
});