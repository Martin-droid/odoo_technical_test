import { Component, mount, useState } from '@odoo/owl';

class Dashboard extends Component {
    static template = 'client_app.Dashboard';

    setup() {
        this.state = useState({
            totalPaidToday: 0,
            upcomingDeliveries: [],
            recentOrders: [],
            overdueInvoices: [],
        });

        this.fetchData();
    }

    async fetchData() {
        this.state.totalPaidToday = await this.fetchTotalPaidToday();
        this.state.upcomingDeliveries = await this.fetchUpcomingDeliveries();
        this.state.recentOrders = await this.fetchRecentOrders();
        this.state.overdueInvoices = await this.fetchOverdueInvoices();
    }

    async fetchTotalPaidToday() {
        // Fetch the data from your model and return the total paid amount
        return 10000;  // Placeholder value
    }

    async fetchUpcomingDeliveries() {
        // Fetch the data from your model and return the list of deliveries
        return [
            { name: 'Order 1', delivery_date: '2024-09-15' },
            { name: 'Order 2', delivery_date: '2024-09-20' },
        ];
    }

    async fetchRecentOrders() {
        // Fetch the data from your model and return the list of recent orders
        return [
            { name: 'Order 1', total_amount: 1500 },
            { name: 'Order 2', total_amount: 2500 },
        ];
    }

    async fetchOverdueInvoices() {
        // Fetch the data from your model and return the list of overdue invoices
        return [
            { name: 'Invoice 1', due_date: '2024-08-30' },
            { name: 'Invoice 2', due_date: '2024-09-05' },
        ];
    }
}

const app = mount(Dashboard, { target: document.body });
