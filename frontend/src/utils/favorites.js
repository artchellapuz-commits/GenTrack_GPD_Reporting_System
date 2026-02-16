// Favorites/Bookmarks Manager

class FavoritesManager {
  constructor() {
    this.storageKey = 'npc_favorites';
    this.favorites = this.load();
  }

  load() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('Error loading favorites:', error);
      return [];
    }
  }

  save() {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(this.favorites));
    } catch (error) {
      console.error('Error saving favorites:', error);
    }
  }

  add(item) {
    // Check if already exists
    const exists = this.favorites.some(f => f.id === item.id && f.type === item.type);
    
    if (!exists) {
      this.favorites.push({
        ...item,
        addedAt: new Date().toISOString()
      });
      this.save();
      return true;
    }
    return false;
  }

  remove(id, type) {
    const index = this.favorites.findIndex(f => f.id === id && f.type === type);
    
    if (index > -1) {
      this.favorites.splice(index, 1);
      this.save();
      return true;
    }
    return false;
  }

  toggle(item) {
    const exists = this.isFavorite(item.id, item.type);
    
    if (exists) {
      this.remove(item.id, item.type);
      return false; // Removed
    } else {
      this.add(item);
      return true; // Added
    }
  }

  isFavorite(id, type) {
    return this.favorites.some(f => f.id === id && f.type === type);
  }

  getAll() {
    return [...this.favorites];
  }

  getByType(type) {
    return this.favorites.filter(f => f.type === type);
  }

  clear() {
    this.favorites = [];
    this.save();
  }

  count() {
    return this.favorites.length;
  }

  // Get recent favorites (last 5)
  getRecent(limit = 5) {
    return [...this.favorites]
      .sort((a, b) => new Date(b.addedAt) - new Date(a.addedAt))
      .slice(0, limit);
  }
}

// Create singleton instance
const favoritesManager = new FavoritesManager();

export default favoritesManager;
