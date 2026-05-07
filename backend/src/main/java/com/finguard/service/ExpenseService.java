package com.finguard.service;

import com.finguard.dto.request.ExpenseRequest;
import com.finguard.dto.response.AnalyticsResponse;
import com.finguard.dto.response.ExpenseResponse;
import com.finguard.dto.response.ExpenseSummaryResponse;
import com.finguard.model.Expense;
import com.finguard.model.User;
import com.finguard.repository.ExpenseRepository;
import com.finguard.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.time.temporal.TemporalAdjusters;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service for expense operations.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class ExpenseService {
    
    private final ExpenseRepository expenseRepository;
    private final UserRepository userRepository;
    
    /**
     * Create a new expense.
     *
     * @param userId the user ID
     * @param request expense request
     * @return created expense response
     */
    @Transactional
    public ExpenseResponse createExpense(Long userId, ExpenseRequest request) {
        log.info("Creating expense for user: {}", userId);
        
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        Expense expense = new Expense();
        expense.setUser(user);
        expense.setCategory(request.getCategory());
        expense.setAmount(request.getAmount());
        expense.setDescription(request.getDescription());
        expense.setExpenseDate(request.getExpenseDate());
        
        expenseRepository.save(expense);
        
        return mapToResponse(expense);
    }
    
    /**
     * Get all expenses for a user with pagination.
     *
     * @param userId the user ID
     * @param pageable pagination info
     * @return page of expense responses
     */
    public Page<ExpenseResponse> getUserExpenses(Long userId, Pageable pageable) {
        return expenseRepository.findByUserId(userId, pageable)
                .map(this::mapToResponse);
    }
    
    /**
     * Get expense summary for a user.
     *
     * @param userId the user ID
     * @return expense summary
     */
    public ExpenseSummaryResponse getExpenseSummary(Long userId) {
        LocalDate now = LocalDate.now();
        LocalDate startOfMonth = now.withDayOfMonth(1);
        LocalDate startOfLastMonth = startOfMonth.minusMonths(1);
        LocalDate endOfLastMonth = startOfMonth.minusDays(1);
        
        // Get totals
        BigDecimal totalThisMonth = expenseRepository.getTotalExpensesByUserAndDateRange(
                userId, startOfMonth, now);
        BigDecimal totalLastMonth = expenseRepository.getTotalExpensesByUserAndDateRange(
                userId, startOfLastMonth, endOfLastMonth);
        
        // Get category breakdown
        List<Object[]> breakdown = expenseRepository.getCategoryBreakdown(
                userId, startOfMonth, now);
        
        List<ExpenseSummaryResponse.CategoryBreakdown> categoryBreakdown = breakdown.stream()
                .map(obj -> ExpenseSummaryResponse.CategoryBreakdown.builder()
                        .category(obj[0].toString())
                        .amount((BigDecimal) obj[1])
                        .percentage(totalThisMonth.compareTo(BigDecimal.ZERO) > 0 ?
                                ((BigDecimal) obj[1]).multiply(BigDecimal.valueOf(100))
                                        .divide(totalThisMonth, 2, RoundingMode.HALF_UP)
                                        .doubleValue() : 0.0)
                        .build())
                .collect(Collectors.toList());
        
        // Calculate month-over-month change
        Double monthOverMonthChange = null;
        if (totalLastMonth.compareTo(BigDecimal.ZERO) > 0) {
            monthOverMonthChange = totalThisMonth.subtract(totalLastMonth)
                    .multiply(BigDecimal.valueOf(100))
                    .divide(totalLastMonth, 2, RoundingMode.HALF_UP)
                    .doubleValue();
        }
        
        // Get top category
        String topCategory = categoryBreakdown.isEmpty() ? null : categoryBreakdown.get(0).getCategory();
        
        return ExpenseSummaryResponse.builder()
                .totalThisMonth(totalThisMonth)
                .totalLastMonth(totalLastMonth)
                .topCategory(topCategory)
                .categoryBreakdown(categoryBreakdown)
                .monthOverMonthChange(monthOverMonthChange)
                .build();
    }
    
    /**
     * Get monthly trend data.
     *
     * @param userId the user ID
     * @param months number of months
     * @return list of monthly totals
     */
    public List<AnalyticsResponse.MonthlyTrend> getMonthlyTrend(Long userId, int months) {
        LocalDate startDate = LocalDate.now().minusMonths(months);
        
        List<Object[]> results = expenseRepository.getMonthlyTotals(userId, startDate);
        
        return results.stream()
                .map(obj -> AnalyticsResponse.MonthlyTrend.builder()
                        .month((String) obj[0])
                        .total((BigDecimal) obj[1])
                        .build())
                .collect(Collectors.toList());
    }
    
    /**
     * Delete an expense.
     *
     * @param userId the user ID
     * @param expenseId the expense ID
     */
    @Transactional
    public void deleteExpense(Long userId, Long expenseId) {
        Expense expense = expenseRepository.findById(expenseId)
                .orElseThrow(() -> new RuntimeException("Expense not found"));
        
        if (!expense.getUser().getId().equals(userId)) {
            throw new RuntimeException("Unauthorized to delete this expense");
        }
        
        expenseRepository.delete(expense);
        log.info("Expense deleted: {}", expenseId);
    }
    
    /**
     * Map Expense entity to ExpenseResponse DTO.
     *
     * @param expense the expense entity
     * @return ExpenseResponse
     */
    private ExpenseResponse mapToResponse(Expense expense) {
        return ExpenseResponse.builder()
                .id(expense.getId())
                .category(expense.getCategory())
                .amount(expense.getAmount())
                .description(expense.getDescription())
                .expenseDate(expense.getExpenseDate())
                .createdAt(expense.getCreatedAt() != null ? expense.getCreatedAt().toString() : null)
                .isAnomaly(false)
                .build();
    }
}
