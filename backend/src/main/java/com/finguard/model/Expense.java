package com.finguard.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/**
 * Expense entity representing a user's expense transaction.
 */
@Entity
@Table(name = "expenses")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Expense {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    @Column(nullable = false, length = 50)
    @Enumerated(EnumType.STRING)
    private ExpenseCategory category;
    
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal amount;
    
    @Column(columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "expense_date", nullable = false)
    private LocalDate expenseDate;
    
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * Constructor for creating a new expense.
     */
    public Expense(User user, ExpenseCategory category, BigDecimal amount, 
                   String description, LocalDate expenseDate) {
        this.user = user;
        this.category = category;
        this.amount = amount;
        this.description = description;
        this.expenseDate = expenseDate;
    }
    
    /**
     * Expense categories.
     */
    public enum ExpenseCategory {
        FOOD,
        TRANSPORT,
        BILLS,
        ENTERTAINMENT,
        HEALTHCARE,
        EDUCATION,
        SHOPPING,
        INVESTMENT,
        SAVINGS,
        OTHER
    }
}
