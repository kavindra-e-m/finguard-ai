package com.finguard.service;

import com.finguard.dto.response.*;
import com.finguard.model.Expense;
import com.finguard.model.User;
import com.finguard.repository.ExpenseRepository;
import com.finguard.repository.InvestmentRepository;
import com.finguard.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Service for analytics operations.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AnalyticsService {
    
    private final ExpenseRepository expenseRepository;
    private final InvestmentRepository investmentRepository;
    private final UserRepository userRepository;
    private final MLService mlService;
    
    /**
     * Predict future expenses for a user.
     *
     * @param userId the user ID
     * @return expense prediction
     */
    public AnalyticsResponse.ExpensePrediction predictExpense(Long userId) {
        log.info("Predicting expenses for user: {}", userId);
        
        // Get last 12 months of expense data
        LocalDate startDate = LocalDate.now().minusMonths(12);
        List<Object[]> monthlyData = expenseRepository.getMonthlyTotals(userId, startDate);
        
        List<Map<String, Object>> monthlyExpenses = monthlyData.stream()
                .map(obj -> {
                    Map<String, Object> map = new HashMap<>();
                    map.put("month", obj[0].toString() + "-01");
                    map.put("amount", ((BigDecimal) obj[1]).doubleValue());
                    return map;
                })
                .collect(Collectors.toList());
        
        return mlService.predictExpense(monthlyExpenses);
    }
    
    /**
     * Detect financial personality for a user.
     *
     * @param userId the user ID
     * @return personality detection result
     */
    public AnalyticsResponse.PersonalityDetection detectPersonality(Long userId) {
        log.info("Detecting personality for user: {}", userId);
        
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        List<Expense> expenses = expenseRepository.findByUserId(userId, null).getContent();
        
        // Calculate features
        BigDecimal monthlyIncome = user.getMonthlyIncome() != null ? 
                user.getMonthlyIncome() : BigDecimal.ZERO;
        
        BigDecimal totalExpenses = expenses.stream()
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        BigDecimal savings = monthlyIncome.subtract(totalExpenses);
        double savingsRatio = monthlyIncome.compareTo(BigDecimal.ZERO) > 0 ?
                savings.divide(monthlyIncome, 4, RoundingMode.HALF_UP).doubleValue() : 0;
        
        // Calculate category ratios
        Map<Expense.ExpenseCategory, BigDecimal> byCategory = expenses.stream()
                .collect(Collectors.groupingBy(
                        Expense::getCategory,
                        Collectors.reducing(BigDecimal.ZERO, Expense::getAmount, BigDecimal::add)
                ));
        
        double foodRatio = getCategoryRatio(byCategory, Expense.ExpenseCategory.FOOD, totalExpenses);
        double entertainmentRatio = getCategoryRatio(byCategory, Expense.ExpenseCategory.ENTERTAINMENT, totalExpenses);
        
        // Get investments count
        int investmentFrequency = investmentRepository.findByUserId(userId).size();
        
        // Calculate average transaction
        double avgTransaction = expenses.isEmpty() ? 0 :
                expenses.stream().mapToDouble(e -> e.getAmount().doubleValue()).average().orElse(0);
        
        Map<String, Object> features = new HashMap<>();
        features.put("savings_ratio", Math.max(0, savingsRatio));
        features.put("expense_variability", 0.15); // Default value
        features.put("investment_frequency", investmentFrequency);
        features.put("risk_exposure", entertainmentRatio);
        features.put("food_ratio", foodRatio);
        features.put("entertainment_ratio", entertainmentRatio);
        features.put("avg_transaction", avgTransaction);
        features.put("monthly_income", monthlyIncome.doubleValue());
        
        return mlService.detectPersonality(features);
    }
    
    /**
     * Predict financial stress for a user.
     *
     * @param userId the user ID
     * @return stress prediction result
     */
    public AnalyticsResponse.StressPrediction predictStress(Long userId) {
        log.info("Predicting stress for user: {}", userId);
        
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        List<Expense> expenses = expenseRepository.findByUserId(userId, null).getContent();
        
        BigDecimal monthlyIncome = user.getMonthlyIncome() != null ? 
                user.getMonthlyIncome() : BigDecimal.ZERO;
        
        BigDecimal totalExpenses = expenses.stream()
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        BigDecimal savings = monthlyIncome.subtract(totalExpenses);
        double savingsRate = monthlyIncome.compareTo(BigDecimal.ZERO) > 0 ?
                savings.divide(monthlyIncome, 4, RoundingMode.HALF_UP).doubleValue() : 0;
        
        // Get last 3 months for trend
        LocalDate threeMonthsAgo = LocalDate.now().minusMonths(3);
        BigDecimal recentExpenses = expenses.stream()
                .filter(e -> e.getExpenseDate().isAfter(threeMonthsAgo))
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        double expenseGrowthRate = totalExpenses.compareTo(BigDecimal.ZERO) > 0 ?
                recentExpenses.subtract(totalExpenses.divide(BigDecimal.valueOf(4), RoundingMode.HALF_UP))
                        .divide(totalExpenses, 4, RoundingMode.HALF_UP).doubleValue() : 0;
        
        Map<String, Object> features = new HashMap<>();
        features.put("debt_to_income_ratio", 0.20); // Default
        features.put("savings_rate", Math.max(0, savingsRate));
        features.put("expense_growth_rate", expenseGrowthRate);
        features.put("income_stability_score", 0.80);
        features.put("emergency_fund_months", 3.0);
        
        return mlService.predictStress(features);
    }
    
    /**
     * Calculate financial health score for a user.
     *
     * @param userId the user ID
     * @return financial health result
     */
    public FinancialHealthResponse calculateFinancialHealth(Long userId) {
        log.info("Calculating financial health for user: {}", userId);
        
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        List<Expense> expenses = expenseRepository.findByUserId(userId, null).getContent();
        
        BigDecimal monthlyIncome = user.getMonthlyIncome() != null ? 
                user.getMonthlyIncome() : BigDecimal.ZERO;
        
        BigDecimal monthlyExpenses = expenses.stream()
                .filter(e -> e.getExpenseDate().isAfter(LocalDate.now().minusMonths(1)))
                .map(Expense::getAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        
        BigDecimal totalSavings = BigDecimal.ZERO; // Would come from user profile
        BigDecimal totalDebt = BigDecimal.ZERO; // Would come from user profile
        
        BigDecimal monthlyInvestments = investmentRepository.getTotalInvestedByUser(userId)
                .divide(BigDecimal.valueOf(12), RoundingMode.HALF_UP);
        
        // Get last 3 months expense trend
        List<Double> expenseTrend = new ArrayList<>();
        for (int i = 2; i >= 0; i--) {
            LocalDate monthStart = LocalDate.now().minusMonths(i).withDayOfMonth(1);
            LocalDate monthEnd = monthStart.plusMonths(1).minusDays(1);
            BigDecimal monthTotal = expenseRepository.getTotalExpensesByUserAndDateRange(
                    userId, monthStart, monthEnd);
            expenseTrend.add(monthTotal.doubleValue());
        }
        
        Map<String, Object> features = new HashMap<>();
        features.put("monthly_income", monthlyIncome.doubleValue());
        features.put("monthly_expenses", monthlyExpenses.doubleValue());
        features.put("total_savings", totalSavings.doubleValue());
        features.put("total_debt", totalDebt.doubleValue());
        features.put("monthly_investments", monthlyInvestments.doubleValue());
        features.put("emergency_fund", totalSavings.doubleValue());
        features.put("expense_trend_3m", expenseTrend);
        
        return mlService.calculateFinancialHealth(features);
    }
    
    /**
     * Detect anomalous expenses for a user.
     *
     * @param userId the user ID
     * @return anomaly detection result
     */
    public AnalyticsResponse.AnomalyDetection detectAnomalies(Long userId) {
        log.info("Detecting anomalies for user: {}", userId);
        
        List<Expense> expenses = expenseRepository.findByUserId(userId, null).getContent();
        
        List<Map<String, Object>> expenseData = expenses.stream()
                .map(e -> {
                    Map<String, Object> map = new HashMap<>();
                    map.put("id", e.getId());
                    map.put("category", e.getCategory().toString());
                    map.put("amount", e.getAmount().doubleValue());
                    map.put("date", e.getExpenseDate().toString());
                    return map;
                })
                .collect(Collectors.toList());
        
        return mlService.detectAnomalies(expenseData);
    }
    
    /**
     * Helper method to calculate category ratio.
     */
    private double getCategoryRatio(Map<Expense.ExpenseCategory, BigDecimal> byCategory, 
                                    Expense.ExpenseCategory category, 
                                    BigDecimal total) {
        if (total.compareTo(BigDecimal.ZERO) == 0) return 0;
        BigDecimal amount = byCategory.getOrDefault(category, BigDecimal.ZERO);
        return amount.divide(total, 4, RoundingMode.HALF_UP).doubleValue();
    }
}
