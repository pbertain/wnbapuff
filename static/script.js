// SportsPuff Web Interface JavaScript

class SportsPuffInterface {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setDefaultDate();
    }

    initializeElements() {
        this.sportSelect = document.getElementById('sport-select');
        this.dataTypeSelect = document.getElementById('data-type-select');
        this.dateInput = document.getElementById('date-input');
        this.seasonInput = document.getElementById('season-input');
        this.searchBtn = document.getElementById('search-btn');
        this.resultsSection = document.getElementById('results-section');
        this.resultsContent = document.getElementById('results-content');
    }

    bindEvents() {
        this.searchBtn.addEventListener('click', () => this.handleSearch());
        
        // Enable search button when both sport and data type are selected
        this.sportSelect.addEventListener('change', () => this.updateSearchButton());
        this.dataTypeSelect.addEventListener('change', () => this.updateSearchButton());
        
        // Enter key support
        document.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && this.isSearchButtonEnabled()) {
                this.handleSearch();
            }
        });
    }

    setDefaultDate() {
        const today = new Date().toISOString().split('T')[0];
        this.dateInput.value = today;
    }

    updateSearchButton() {
        const sportSelected = this.sportSelect.value !== '';
        const dataTypeSelected = this.dataTypeSelect.value !== '';
        
        if (sportSelected && dataTypeSelected) {
            this.searchBtn.disabled = false;
            this.searchBtn.style.opacity = '1';
        } else {
            this.searchBtn.disabled = true;
            this.searchBtn.style.opacity = '0.6';
        }
    }

    isSearchButtonEnabled() {
        return this.sportSelect.value !== '' && this.dataTypeSelect.value !== '';
    }

    async handleSearch() {
        if (!this.isSearchButtonEnabled()) {
            this.showError('Please select both a sport and data type.');
            return;
        }

        const sport = this.sportSelect.value;
        const dataType = this.dataTypeSelect.value;
        const date = this.dateInput.value;
        const season = this.seasonInput.value;

        this.setLoadingState(true);
        this.hideResults();

        try {
            const url = this.buildApiUrl(sport, dataType, date, season);
            const response = await this.fetchData(url);
            
            if (response.ok) {
                const data = await response.text();
                this.showResults(data, sport, dataType);
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        } catch (error) {
            console.error('API Error:', error);
            this.showError(`Failed to fetch data: ${error.message}`);
        } finally {
            this.setLoadingState(false);
        }
    }

    buildApiUrl(sport, dataType, date, season) {
        const baseUrl = window.location.origin;
        let url = `${baseUrl}/curl/${sport}/${dataType}`;
        
        const params = new URLSearchParams();
        
        if (date) {
            params.append('date', date);
        }
        
        if (season) {
            params.append('season', season);
        }
        
        if (dataType === 'standings') {
            params.append('group', 'conference');
        }
        
        if (params.toString()) {
            url += `?${params.toString()}`;
        }
        
        return url;
    }

    async fetchData(url) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
        
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Accept': 'text/plain, application/json',
                    'User-Agent': 'SportsPuff-Web-Interface/1.0'
                },
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error('Request timed out');
            }
            throw error;
        }
    }

    setLoadingState(loading) {
        if (loading) {
            this.searchBtn.innerHTML = '<span class="loading"></span> Loading...';
            this.searchBtn.disabled = true;
        } else {
            this.searchBtn.innerHTML = 'Get Data';
            this.updateSearchButton();
        }
    }

    showResults(data, sport, dataType) {
        const sportName = sport.toUpperCase();
        const dataTypeName = dataType.charAt(0).toUpperCase() + dataType.slice(1);
        
        this.resultsContent.innerHTML = `
            <div class="success">
                <strong>${sportName} ${dataTypeName}</strong>
                <br><br>
                ${this.escapeHtml(data)}
            </div>
        `;
        
        this.resultsSection.style.display = 'block';
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showError(message) {
        this.resultsContent.innerHTML = `
            <div class="error">
                <strong>Error:</strong> ${this.escapeHtml(message)}
            </div>
        `;
        
        this.resultsSection.style.display = 'block';
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Utility method to get current API status
    async checkApiStatus() {
        try {
            const response = await fetch('/curl/wnba/help');
            return response.ok;
        } catch (error) {
            console.warn('API status check failed:', error);
            return false;
        }
    }
}

// Initialize the interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const interface = new SportsPuffInterface();
    
    // Check API status on load
    interface.checkApiStatus().then(isOnline => {
        if (!isOnline) {
            console.warn('SportsPuff API appears to be offline');
        }
    });
    
    // Make interface available globally for debugging
    window.sportsPuffInterface = interface;
});

// Add some fun sports-themed console messages
console.log(`
🏀 SportsPuff Web Interface Loaded! 🏈
⚾ Ready to fetch sports data! ⚽
🏒 Visit https://sportpuff.net for more info! 🏀
`); 