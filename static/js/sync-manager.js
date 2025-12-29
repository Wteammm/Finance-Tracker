// Finance Tracker - Sync Manager
// Handles automatic synchronization of offline data

class SyncManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.isSyncing = false;
        this.syncInterval = null;
        this.statusCallbacks = [];
    }

    // Initialize sync manager
    async init() {
        // Initialize offline database
        await offlineDB.init();

        // Listen for online/offline events
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());

        // Check if we have pending items and we're online
        if (this.isOnline) {
            await this.syncAll();
        }

        // Update UI
        this.updateStatus();

        // Periodic check for pending items (every 30 seconds)
        this.syncInterval = setInterval(() => {
            if (this.isOnline && !this.isSyncing) {
                this.syncAll();
            }
        }, 30000);
    }

    // Handle coming back online
    async handleOnline() {
        console.log('Connection restored - syncing offline data...');
        this.isOnline = true;
        this.updateStatus();
        await this.syncAll();
    }

    // Handle going offline
    handleOffline() {
        console.log('Connection lost - entering offline mode');
        this.isOnline = false;
        this.updateStatus();
    }

    // Sync all pending data
    async syncAll() {
        if (this.isSyncing || !this.isOnline) return;

        this.isSyncing = true;
        this.updateStatus();

        try {
            // Sync transactions
            await this.syncTransactions();

            // Sync investments
            await this.syncInvestments();

            // Sync balance items
            await this.syncBalanceItems();

            // Clean up synced items
            await this.cleanupSynced();

            console.log('Sync completed successfully');
            this.showNotification('✅ All data synced successfully', 'success');
        } catch (error) {
            console.error('Sync failed:', error);
            this.showNotification('⚠️ Sync failed. Will retry automatically.', 'warning');
        } finally {
            this.isSyncing = false;
            this.updateStatus();
        }
    }

    // Sync transactions
    async syncTransactions() {
        const pending = await offlineDB.getPendingTransactions();
        if (pending.length === 0) return;

        console.log(`Syncing ${pending.length} transactions...`);

        for (const item of pending) {
            try {
                const response = await fetch('/api/sync/transaction', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(item)
                });

                if (response.ok) {
                    await offlineDB.markSynced('transactions', item.id);
                } else {
                    console.error('Failed to sync transaction:', item.id);
                }
            } catch (error) {
                console.error('Error syncing transaction:', error);
                throw error;
            }
        }
    }

    // Sync investments
    async syncInvestments() {
        const pending = await offlineDB.getPendingInvestments();
        if (pending.length === 0) return;

        console.log(`Syncing ${pending.length} investments...`);

        for (const item of pending) {
            try {
                const response = await fetch('/api/sync/investment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(item)
                });

                if (response.ok) {
                    await offlineDB.markSynced('investments', item.id);
                } else {
                    console.error('Failed to sync investment:', item.id);
                }
            } catch (error) {
                console.error('Error syncing investment:', error);
                throw error;
            }
        }
    }

    // Sync balance items
    async syncBalanceItems() {
        const pending = await offlineDB.getPendingBalanceItems();
        if (pending.length === 0) return;

        console.log(`Syncing ${pending.length} balance items...`);

        for (const item of pending) {
            try {
                const response = await fetch('/api/sync/balance_item', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(item)
                });

                if (response.ok) {
                    await offlineDB.markSynced('balanceItems', item.id);
                } else {
                    console.error('Failed to sync balance item:', item.id);
                }
            } catch (error) {
                console.error('Error syncing balance item:', error);
                throw error;
            }
        }
    }

    // Clean up synced items
    async cleanupSynced() {
        await offlineDB.clearSynced('transactions');
        await offlineDB.clearSynced('investments');
        await offlineDB.clearSynced('balanceItems');
    }

    // Update status UI
    async updateStatus() {
        const pendingCount = await offlineDB.getPendingCount();

        const statusData = {
            isOnline: this.isOnline,
            isSyncing: this.isSyncing,
            pendingCount: pendingCount
        };

        // Update status indicator
        this.updateStatusIndicator(statusData);

        // Call registered callbacks
        this.statusCallbacks.forEach(callback => callback(statusData));
    }

    // Update status indicator in UI
    updateStatusIndicator(status) {
        const indicator = document.getElementById('syncStatus');
        if (!indicator) return;

        let html = '';

        if (!status.isOnline) {
            html = '<span class="badge bg-danger">🔴 Offline</span>';
            if (status.pendingCount > 0) {
                html += ` <span class="badge bg-warning">⚠️ ${status.pendingCount} pending</span>`;
            }
        } else if (status.isSyncing) {
            html = '<span class="badge bg-primary">🟢 Online</span> <span class="badge bg-info">⏳ Syncing...</span>';
        } else if (status.pendingCount > 0) {
            html = '<span class="badge bg-primary">🟢 Online</span> <span class="badge bg-warning">⚠️ ${status.pendingCount} pending</span>';
        } else {
            html = '<span class="badge bg-success">🟢 Online</span> <span class="badge bg-success">✅ Synced</span>';
        }

        indicator.innerHTML = html;
    }

    // Show notification
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 70px; right: 20px; z-index: 9999; min-width: 200px; max-width: 300px; padding: 0.5rem 0.75rem; font-size: 0.85rem;';
        notification.innerHTML = `
      ${message}
      <button type="button" class="btn-close btn-close-sm" data-bs-dismiss="alert" style="font-size: 0.7rem; padding: 0.25rem;"></button>
    `;

        document.body.appendChild(notification);

        // Auto-remove after 3 seconds (reduced from 5)
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Register status callback
    onStatusChange(callback) {
        this.statusCallbacks.push(callback);
    }

    // Manual sync trigger
    async manualSync() {
        if (!this.isOnline) {
            this.showNotification('⚠️ Cannot sync while offline', 'warning');
            return;
        }

        this.showNotification('🔄 Starting sync...', 'info');
        await this.syncAll();
    }
}

// Export singleton instance
const syncManager = new SyncManager();
