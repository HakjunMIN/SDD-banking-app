/**
 * Date utility functions for banking app
 * Provides date manipulation and formatting functions for transaction filtering
 */

export const dateUtils = {
  /**
   * Get today's date range (same day for both from and to)
   */
  getToday: () => {
    const today = new Date();
    const dateString = today.toISOString().split('T')[0];
    return {
      fromDate: dateString,
      toDate: dateString
    };
  },

  /**
   * Get yesterday's date range
   */
  getYesterday: () => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const dateString = yesterday.toISOString().split('T')[0];
    return {
      fromDate: dateString,
      toDate: dateString
    };
  },

  /**
   * Get date range for the last N days (including today)
   */
  getLastDays: (days: number) => {
    const today = new Date();
    const startDate = new Date();
    startDate.setDate(today.getDate() - (days - 1));
    
    return {
      fromDate: startDate.toISOString().split('T')[0],
      toDate: today.toISOString().split('T')[0]
    };
  },

  /**
   * Get current month date range (from 1st to today or last day of month)
   */
  getCurrentMonth: () => {
    const now = new Date();
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    
    return {
      fromDate: firstDay.toISOString().split('T')[0],
      toDate: Math.min(now.getTime(), lastDay.getTime()) === now.getTime() 
        ? now.toISOString().split('T')[0]
        : lastDay.toISOString().split('T')[0]
    };
  },

  /**
   * Get last month date range (full month)
   */
  getLastMonth: () => {
    const now = new Date();
    const firstDay = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const lastDay = new Date(now.getFullYear(), now.getMonth(), 0);
    
    return {
      fromDate: firstDay.toISOString().split('T')[0],
      toDate: lastDay.toISOString().split('T')[0]
    };
  },

  /**
   * Get date range for the last N months (including current month up to today)
   */
  getLastMonths: (months: number) => {
    const today = new Date();
    const startDate = new Date();
    startDate.setMonth(today.getMonth() - (months - 1));
    startDate.setDate(1); // Start from first day of the month
    
    return {
      fromDate: startDate.toISOString().split('T')[0],
      toDate: today.toISOString().split('T')[0]
    };
  },

  /**
   * Format date for display (Korean format)
   */
  formatDisplayDate: (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'short'
    });
  },

  /**
   * Get relative date description (e.g., "3 days ago", "1 week ago")
   */
  getRelativeDate: (dateString: string): string => {
    const date = new Date(dateString);
    const today = new Date();
    const diffTime = today.getTime() - date.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return '오늘';
    if (diffDays === 1) return '어제';
    if (diffDays < 7) return `${diffDays}일 전`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)}주 전`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)}개월 전`;
    return `${Math.floor(diffDays / 365)}년 전`;
  },

  /**
   * Check if a date string is valid
   */
  isValidDate: (dateString: string): boolean => {
    const date = new Date(dateString);
    return !isNaN(date.getTime()) && !!dateString.match(/^\d{4}-\d{2}-\d{2}$/);
  },

  /**
   * Check if from_date is before or equal to to_date
   */
  isValidDateRange: (fromDate: string, toDate: string): boolean => {
    if (!dateUtils.isValidDate(fromDate) || !dateUtils.isValidDate(toDate)) {
      return false;
    }
    
    const from = new Date(fromDate);
    const to = new Date(toDate);
    return from <= to;
  },

  /**
   * Get the number of days between two dates
   */
  getDaysBetween: (fromDate: string, toDate: string): number => {
    const from = new Date(fromDate);
    const to = new Date(toDate);
    const diffTime = to.getTime() - from.getTime();
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  },

  /**
   * Get today's date in YYYY-MM-DD format
   */
  getTodayString: (): string => {
    return new Date().toISOString().split('T')[0];
  },

  /**
   * Get date N days ago in YYYY-MM-DD format
   */
  getDaysAgoString: (days: number): string => {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date.toISOString().split('T')[0];
  }
};