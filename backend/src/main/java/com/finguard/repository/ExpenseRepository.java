package com.finguard.repository;

import com.finguard.model.Expense;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

/**
 * Repository for Expense entity operations.
 */
@Repository
public interface ExpenseRepository extends JpaRepository<Expense, Long> {
    
    /**
     * Find all expenses for a user with pagination.
     *
     * @param userId the user ID
     * @param pageable pagination information
     * @return page of expenses
     */
    Page<Expense> findByUserId(Long userId, Pageable pageable);
    
    /**
     * Find expenses by user and category.
     *
     * @param userId the user ID
     * @param category the expense category
     * @return list of expenses
     */
    List<Expense> findByUserIdAndCategory(Long userId, Expense.ExpenseCategory category);
    
    /**
     * Find expenses within date range.
     *
     * @param userId the user ID
     * @param startDate start date
     * @param endDate end date
     * @return list of expenses
     */
    List<Expense> findByUserIdAndExpenseDateBetween(Long userId, LocalDate startDate, LocalDate endDate);
    
    /**
     * Get total expenses for a user in a date range.
     *
     * @param userId the user ID
     * @param startDate start date
     * @param endDate end date
     * @return total amount
     */
    @Query("SELECT COALESCE(SUM(e.amount), 0) FROM Expense e WHERE e.user.id = :userId AND e.expenseDate BETWEEN :startDate AND :endDate")
    BigDecimal getTotalExpensesByUserAndDateRange(@Param("userId") Long userId, 
                                                   @Param("startDate") LocalDate startDate, 
                                                   @Param("endDate") LocalDate endDate);
    
    /**
     * Get category breakdown for a user.
     *
     * @param userId the user ID
     * @param startDate start date
     * @param endDate end date
     * @return list of category and amount tuples
     */
    @Query("SELECT e.category, SUM(e.amount) FROM Expense e WHERE e.user.id = :userId AND e.expenseDate BETWEEN :startDate AND :endDate GROUP BY e.category ORDER BY SUM(e.amount) DESC")
    List<Object[]> getCategoryBreakdown(@Param("userId") Long userId, 
                                        @Param("startDate") LocalDate startDate, 
                                        @Param("endDate") LocalDate endDate);
    
    /**
     * Get monthly expense totals.
     *
     * @param userId the user ID
     * @param startDate start date
     * @return list of month and total tuples
     */
    @Query(value = "SELECT TO_CHAR(e.expense_date, 'YYYY-MM') as month, SUM(e.amount) as total " +
                   "FROM expenses e WHERE e.user_id = :userId AND e.expense_date >= :startDate " +
                   "GROUP BY TO_CHAR(e.expense_date, 'YYYY-MM') ORDER BY month", 
           nativeQuery = true)
    List<Object[]> getMonthlyTotals(@Param("userId") Long userId, @Param("startDate") LocalDate startDate);
}
