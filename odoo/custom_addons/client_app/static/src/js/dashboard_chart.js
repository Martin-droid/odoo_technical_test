/** @odoo-module **/

import { Component } from "@odoo/owl";

class PaymentBarChart extends Component {
    static template = "client_app.PaymentBarChart";

    async willStart() {
        // Fetch payment data from the backend
        const paymentsData = await this.loadPaymentData();
        this.chartData = this.processData(paymentsData);
    }

    async loadPaymentData() {
        // RPC to fetch payment data (payment_date and amount)
        return await this.env.services.rpc({
            model: "client.app.payment",
            method: "search_read",
            args: [[], ["payment_date", "amount"]],
        });
    }

    processData(data) {
        // Group payments by date and calculate total amount per day
        const result = {};
        data.forEach(payment => {
            const date = payment.payment_date;
            if (!result[date]) {
                result[date] = 0;
            }
            result[date] += payment.amount;
        });
        return result;
    }

    mounted() {
        const ctx = this.el.querySelector("#paymentBarChart").getContext("2d");

        // Create labels and data for the chart
        const labels = Object.keys(this.chartData);
        const values = Object.values(this.chartData);

        // Render the bar chart
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "Total Payments per Day",
                        data: values,
                        backgroundColor: "rgba(75, 192, 192, 0.6)",
                        borderColor: "rgba(75, 192, 192, 1)",
                        borderWidth: 1,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });
    }
}

export default PaymentBarChart;
