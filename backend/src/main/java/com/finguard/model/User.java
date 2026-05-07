package com.finguard.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * User entity representing a FinGuard AI user.
 */
@Entity
@Table(name = "users")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 100)
    private String name;
    
    @Column(nullable = false, unique = true, length = 150)
    private String email;
    
    @Column(nullable = false, length = 255)
    private String password;
    
    @Column(name = "monthly_income", precision = 12, scale = 2)
    private BigDecimal monthlyIncome = BigDecimal.ZERO;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Expense> expenses = new ArrayList<>();
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Investment> investments = new ArrayList<>();
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Prediction> predictions = new ArrayList<>();
    
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    /**
     * Constructor for creating a new user.
     */
    public User(String name, String email, String password, BigDecimal monthlyIncome) {
        this.name = name;
        this.email = email;
        this.password = password;
        this.monthlyIncome = monthlyIncome != null ? monthlyIncome : BigDecimal.ZERO;
    }
}
