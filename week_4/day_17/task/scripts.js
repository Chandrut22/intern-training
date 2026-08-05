const form = document.getElementById('user-input');
const container = document.getElementById('table-container');
const paginationContainer = document.getElementById('pagination-container');

let allData = [];          
let currentPage = 1;       
const rowsPerPage = 10;   

form.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(form);
    const country = formData.get('country') || '';
    const university = formData.get('university') || '';

    const url = `http://universities.hipolabs.com/search?name=${encodeURIComponent(university)}&country=${encodeURIComponent(country)}`;

    paginationContainer.innerHTML = "";
    allData = [];
    currentPage = 1;

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error("Network response is not ok");
            return response.json();
        })
        .then(data => {
            allData = data;
            renderPage(currentPage);
        })
        .catch(error => {
            console.error("Fetch error: ", error);
            container.innerHTML = "<h2>Error fetching university records. Please try again.</h2>";
        });
});

function renderPage(page) {
    container.innerHTML = "";
    
    if (!allData || allData.length === 0) {
        container.innerHTML = "<h2>No Data Available</h2>";
        paginationContainer.innerHTML = "";
        return;
    }

    // Math calculation for pagination bounds
    const startIndex = (page - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const paginatedItems = allData.slice(startIndex, endIndex);

    // Build and insert the subset table
    const table = generateTable(paginatedItems, startIndex + 1);
    if (table) {
        container.appendChild(table);
    }

    setupPaginationControls();
}

function generateTable(data, startingNumber) {
    const table = document.createElement('table');
    const headerRow = document.createElement('tr');
    
    const headers = ["No.", "Website Link", "Name", "Country", "Country Code", "Domain"];
    headers.forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    data.forEach((item, index) => {
        const row = document.createElement('tr');

        const rowNo = startingNumber + index;
        const webPage = item.web_pages ? item.web_pages[0] : '';
        const name = item.name || '';
        const country = item.country || '';
        const countryCode = item.alpha_two_code || '';
        const domain = item.domains ? item.domains[0] : '';

        const rowData = [rowNo, webPage, name, country, countryCode, domain];

        rowData.forEach(value => {
            const td = document.createElement('td');
            td.textContent = value;
            row.appendChild(td);
        });

        table.appendChild(row);
    });

    return table;
}

function setupPaginationControls() {
    paginationContainer.innerHTML = "";
    const totalPages = Math.ceil(allData.length / rowsPerPage);

    if (totalPages <= 1) return; 

    // 1. Prev Button
    const prevBtn = document.createElement('button');
    prevBtn.textContent = "Prev";
    prevBtn.disabled = currentPage === 1;
    prevBtn.addEventListener('click', () => {
        currentPage--;
        renderPage(currentPage);
    });
    paginationContainer.appendChild(prevBtn);

    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    for (let i = startPage; i <= endPage; i++) {
        const pageBtn = document.createElement('button');
        pageBtn.textContent = i;
        if (i === currentPage) {
            pageBtn.classList.add('active'); 
        }
        pageBtn.addEventListener('click', () => {
            currentPage = i;
            renderPage(currentPage);
        });
        paginationContainer.appendChild(pageBtn);
    }

    const nextBtn = document.createElement('button');
    nextBtn.textContent = "Next";
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.addEventListener('click', () => {
        currentPage++;
        renderPage(currentPage);
    });
    paginationContainer.appendChild(nextBtn);
}