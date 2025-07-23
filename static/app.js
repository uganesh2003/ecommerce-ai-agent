// E-commerce AI Data Agent - Frontend JavaScript

class EcommerceAIAgent {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadExampleQuestions();
        this.loadDataSummary();
    }

    setupEventListeners() {
        // Main question form
        const questionForm = document.getElementById('questionForm');
        if (questionForm) {
            questionForm.addEventListener('submit', (e) => this.handleQuestionSubmit(e));
        }

        // Quick question buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-question') || e.target.closest('.quick-question')) {
                const button = e.target.classList.contains('quick-question') ? e.target : e.target.closest('.quick-question');
                const question = button.dataset.question;
                if (question) {
                    this.askQuestion(question);
                }
            }

            // Example question clicks
            if (e.target.classList.contains('example-question') || e.target.closest('.example-question')) {
                const questionElement = e.target.classList.contains('example-question') ? e.target : e.target.closest('.example-question');
                const question = questionElement.dataset.question;
                if (question) {
                    document.getElementById('questionInput').value = question;
                    document.getElementById('questionInput').focus();
                }
            }
        });
    }

    async handleQuestionSubmit(e) {
        e.preventDefault();
        
        const questionInput = document.getElementById('questionInput');
        const question = questionInput.value.trim();
        
        if (!question) {
            this.showError('Please enter a question');
            return;
        }

        await this.askQuestion(question);
    }

    async askQuestion(question) {
        try {
            this.showLoading(true);
            this.hideResponse();

            // Update question input if it's different
            const questionInput = document.getElementById('questionInput');
            if (questionInput.value !== question) {
                questionInput.value = question;
            }

            const response = await fetch('/api/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            const result = await response.json();
            
            if (result.success) {
                this.showResponse(result);
            } else {
                this.showError(result.error || 'An error occurred while processing your question');
            }

        } catch (error) {
            console.error('Error asking question:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    showResponse(result) {
        const container = document.getElementById('responseContainer');
        
        const responseHtml = `
            <div class="card response-card shadow typing-animation">
                <div class="card-body p-4">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <h6 class="card-title text-success mb-0">
                            <i class="fas fa-check-circle me-2"></i>
                            Response
                        </h6>
                        <small class="text-muted">
                            <i class="fas fa-clock me-1"></i>
                            ${new Date().toLocaleTimeString()}
                        </small>
                    </div>
                    
                    <div class="mb-3">
                        <strong class="text-primary">Question:</strong>
                        <p class="mb-2">${this.escapeHtml(result.question)}</p>
                    </div>
                    
                    <div class="mb-3">
                        <strong class="text-success">Answer:</strong>
                        <div class="mt-2 p-3 bg-dark rounded border">
                            ${this.formatAnswer(result.formatted_answer)}
                        </div>
                    </div>
                    
                    ${result.sql_query ? `
                        <div class="collapse" id="technicalDetails">
                            <div class="border-top pt-3">
                                <div class="mb-3">
                                    <strong class="text-info">Generated SQL Query:</strong>
                                    <pre class="mt-2 p-2 bg-secondary rounded"><code>${this.escapeHtml(result.sql_query)}</code></pre>
                                </div>
                                
                                ${result.explanation ? `
                                    <div class="mb-3">
                                        <strong class="text-warning">Explanation:</strong>
                                        <p class="mt-2 small text-muted">${this.escapeHtml(result.explanation)}</p>
                                    </div>
                                ` : ''}
                                
                                ${result.raw_result && result.raw_result.length > 0 ? `
                                    <div class="mb-3">
                                        <strong class="text-secondary">Raw Data:</strong>
                                        <div class="mt-2 p-2 bg-secondary rounded small">
                                            <pre><code>${JSON.stringify(result.raw_result, null, 2)}</code></pre>
                                        </div>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                        
                        <button class="btn btn-outline-secondary btn-sm" type="button" data-bs-toggle="collapse" data-bs-target="#technicalDetails">
                            <i class="fas fa-code me-1"></i>
                            Show Technical Details
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
        
        container.innerHTML = responseHtml;
        container.style.display = 'block';
        
        // Scroll to response
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    showError(message) {
        const container = document.getElementById('responseContainer');
        
        const errorHtml = `
            <div class="card error-card shadow typing-animation">
                <div class="card-body p-4">
                    <h6 class="card-title text-danger mb-3">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Error
                    </h6>
                    <p class="text-muted mb-0">${this.escapeHtml(message)}</p>
                </div>
            </div>
        `;
        
        container.innerHTML = errorHtml;
        container.style.display = 'block';
        
        // Scroll to error
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    hideResponse() {
        const container = document.getElementById('responseContainer');
        container.style.display = 'none';
    }

    showLoading(show) {
        const spinner = document.querySelector('.loading-spinner');
        const submitBtn = document.querySelector('#questionForm button[type="submit"]');
        const quickBtns = document.querySelectorAll('.quick-question');
        
        if (show) {
            spinner.style.display = 'flex';
            submitBtn.disabled = true;
            quickBtns.forEach(btn => btn.disabled = true);
        } else {
            spinner.style.display = 'none';
            submitBtn.disabled = false;
            quickBtns.forEach(btn => btn.disabled = false);
        }
    }

    async loadExampleQuestions() {
        try {
            const response = await fetch('/api/examples');
            const result = await response.json();
            
            if (result.success && result.examples) {
                this.renderExampleQuestions(result.examples);
            } else {
                document.getElementById('exampleQuestions').innerHTML = 
                    '<p class="text-muted small">Failed to load example questions</p>';
            }
        } catch (error) {
            console.error('Error loading examples:', error);
            document.getElementById('exampleQuestions').innerHTML = 
                '<p class="text-muted small">Failed to load example questions</p>';
        }
    }

    renderExampleQuestions(examples) {
        const container = document.getElementById('exampleQuestions');
        
        const examplesHtml = examples.map(example => `
            <div class="example-question p-2 rounded border mb-2" 
                 data-question="${this.escapeHtml(example.question)}"
                 role="button"
                 tabindex="0">
                <div class="d-flex align-items-start">
                    <i class="fas fa-question-circle text-primary me-2 mt-1"></i>
                    <div>
                        <strong class="small">${this.escapeHtml(example.question)}</strong>
                        <div class="small text-muted">${this.escapeHtml(example.description)}</div>
                    </div>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = examplesHtml;
    }

    async loadDataSummary() {
        try {
            const response = await fetch('/api/data/summary');
            const result = await response.json();
            
            if (result.success && result.summary) {
                this.renderDataSummary(result.summary);
            } else {
                document.getElementById('dataSummary').innerHTML = 
                    '<p class="text-muted small">Failed to load data summary</p>';
            }
        } catch (error) {
            console.error('Error loading data summary:', error);
            document.getElementById('dataSummary').innerHTML = 
                '<p class="text-muted small">Failed to load data summary</p>';
        }
    }

    renderDataSummary(summary) {
        const container = document.getElementById('dataSummary');
        
        const summaryHtml = `
            <div class="row g-3">
                <div class="col-md-4">
                    <div class="text-center p-2 bg-primary bg-opacity-10 rounded">
                        <div class="h4 text-primary mb-1">${summary.total_products || 0}</div>
                        <small class="text-muted">Products</small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="text-center p-2 bg-success bg-opacity-10 rounded">
                        <div class="h4 text-success mb-1">${summary.total_sales_records || 0}</div>
                        <small class="text-muted">Sales Records</small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="text-center p-2 bg-info bg-opacity-10 rounded">
                        <div class="h4 text-info mb-1">${summary.total_ad_records || 0}</div>
                        <small class="text-muted">Ad Records</small>
                    </div>
                </div>
            </div>
            
            ${summary.date_range && summary.date_range.sales_start ? `
                <div class="mt-3 text-center">
                    <small class="text-muted">
                        <i class="fas fa-calendar me-1"></i>
                        Data Range: ${summary.date_range.sales_start} to ${summary.date_range.sales_end}
                    </small>
                </div>
            ` : ''}
        `;
        
        container.innerHTML = summaryHtml;
    }

    formatAnswer(answer) {
        // Simple formatting for better readability
        if (!answer) return 'No answer provided';
        
        // Convert line breaks to HTML
        let formatted = this.escapeHtml(answer).replace(/\n/g, '<br>');
        
        // Make numbers stand out
        formatted = formatted.replace(/\$[\d,]+\.?\d*/g, '<strong class="text-success">$&</strong>');
        formatted = formatted.replace(/\b\d+\.?\d*%/g, '<strong class="text-info">$&</strong>');
        
        return formatted;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EcommerceAIAgent();
});
