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
 * Prediction entity for storing ML prediction results.
 */
@Entity
@Table(name = "predictions")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Prediction {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    
    @Column(name = "prediction_type", nullable = false, length = 50)
    @Enumerated(EnumType.STRING)
    private PredictionType predictionType;
    
    @Column(name = "predicted_value", precision = 12, scale = 2)
    private BigDecimal predictedValue;
    
    @Column(name = "prediction_label", length = 100)
    private String predictionLabel;
    
    @Column(precision = 5, scale = 4)
    private BigDecimal confidence;
    
    @Column(name = "prediction_date", nullable = false)
    private LocalDate predictionDate;
    
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    /**
     * Constructor for creating a new prediction record.
     */
    public Prediction(User user, PredictionType predictionType, BigDecimal predictedValue,
                      String predictionLabel, BigDecimal confidence, LocalDate predictionDate) {
        this.user = user;
        this.predictionType = predictionType;
        this.predictedValue = predictedValue;
        this.predictionLabel = predictionLabel;
        this.confidence = confidence;
        this.predictionDate = predictionDate;
    }
    
    /**
     * Prediction types.
     */
    public enum PredictionType {
        EXPENSE,
        STRESS,
        PERSONALITY,
        HEALTH_SCORE
    }
}
