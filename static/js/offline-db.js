// Finance Tracker - Offline Database Manager
// Manages IndexedDB for storing offline data

class OfflineDB {
  constructor() {
    this.dbName = 'FinanceTrackerDB';
    this.version = 1;
    this.db = null;
  }

  // Initialize database
  async init() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, this.version);

      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Create object stores for different data types
        if (!db.objectStoreNames.contains('transactions')) {
          const transactionStore = db.createObjectStore('transactions', { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          transactionStore.createIndex('syncStatus', 'syncStatus', { unique: false });
          transactionStore.createIndex('timestamp', 'timestamp', { unique: false });
        }

        if (!db.objectStoreNames.contains('investments')) {
          const investmentStore = db.createObjectStore('investments', { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          investmentStore.createIndex('syncStatus', 'syncStatus', { unique: false });
          investmentStore.createIndex('timestamp', 'timestamp', { unique: false });
        }

        if (!db.objectStoreNames.contains('balanceItems')) {
          const balanceStore = db.createObjectStore('balanceItems', { 
            keyPath: 'id', 
            autoIncrement: true 
          });
          balanceStore.createIndex('syncStatus', 'syncStatus', { unique: false });
          balanceStore.createIndex('timestamp', 'timestamp', { unique: false });
        }
      };
    });
  }

  // Add transaction to offline storage
  async addTransaction(data) {
    const transaction = this.db.transaction(['transactions'], 'readwrite');
    const store = transaction.objectStore('transactions');
    
    const item = {
      ...data,
      syncStatus: 'pending',
      timestamp: new Date().toISOString()
    };

    return new Promise((resolve, reject) => {
      const request = store.add(item);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  // Add investment to offline storage
  async addInvestment(data) {
    const transaction = this.db.transaction(['investments'], 'readwrite');
    const store = transaction.objectStore('investments');
    
    const item = {
      ...data,
      syncStatus: 'pending',
      timestamp: new Date().toISOString()
    };

    return new Promise((resolve, reject) => {
      const request = store.add(item);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  // Add balance item to offline storage
  async addBalanceItem(data) {
    const transaction = this.db.transaction(['balanceItems'], 'readwrite');
    const store = transaction.objectStore('balanceItems');
    
    const item = {
      ...data,
      syncStatus: 'pending',
      timestamp: new Date().toISOString()
    };

    return new Promise((resolve, reject) => {
      const request = store.add(item);
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  // Get all pending items from a store
  async getPending(storeName) {
    const transaction = this.db.transaction([storeName], 'readonly');
    const store = transaction.objectStore(storeName);
    const index = store.index('syncStatus');

    return new Promise((resolve, reject) => {
      const request = index.getAll('pending');
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  // Get all pending transactions
  async getPendingTransactions() {
    return this.getPending('transactions');
  }

  // Get all pending investments
  async getPendingInvestments() {
    return this.getPending('investments');
  }

  // Get all pending balance items
  async getPendingBalanceItems() {
    return this.getPending('balanceItems');
  }

  // Get count of all pending items
  async getPendingCount() {
    const transactions = await this.getPendingTransactions();
    const investments = await this.getPendingInvestments();
    const balanceItems = await this.getPendingBalanceItems();
    
    return transactions.length + investments.length + balanceItems.length;
  }

  // Mark item as synced
  async markSynced(storeName, id) {
    const transaction = this.db.transaction([storeName], 'readwrite');
    const store = transaction.objectStore(storeName);

    return new Promise((resolve, reject) => {
      const getRequest = store.get(id);
      
      getRequest.onsuccess = () => {
        const item = getRequest.result;
        if (item) {
          item.syncStatus = 'synced';
          const updateRequest = store.put(item);
          updateRequest.onsuccess = () => resolve();
          updateRequest.onerror = () => reject(updateRequest.error);
        } else {
          resolve(); // Item doesn't exist, nothing to update
        }
      };
      
      getRequest.onerror = () => reject(getRequest.error);
    });
  }

  // Delete synced item
  async deleteSynced(storeName, id) {
    const transaction = this.db.transaction([storeName], 'readwrite');
    const store = transaction.objectStore(storeName);

    return new Promise((resolve, reject) => {
      const request = store.delete(id);
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  // Clear all synced items
  async clearSynced(storeName) {
    const transaction = this.db.transaction([storeName], 'readwrite');
    const store = transaction.objectStore(storeName);
    const index = store.index('syncStatus');

    return new Promise((resolve, reject) => {
      const request = index.openCursor(IDBKeyRange.only('synced'));
      
      request.onsuccess = (event) => {
        const cursor = event.target.result;
        if (cursor) {
          cursor.delete();
          cursor.continue();
        } else {
          resolve();
        }
      };
      
      request.onerror = () => reject(request.error);
    });
  }
}

// Export singleton instance
const offlineDB = new OfflineDB();
