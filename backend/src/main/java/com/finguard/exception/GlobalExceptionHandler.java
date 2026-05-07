package com.finguard.exception;

import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Global exception handler for REST controllers.
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    /**
     * Handle validation errors.
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationErrors(
            MethodArgumentNotValidException ex) {
        
        Map<String, String> errors = new HashMap<>();
        StringBuilder message = new StringBuilder();
        
        ex.getBindingResult().getAllErrors().forEach(error -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
            
            if (message.length() > 0) {
                message.append(", ");
            }
            message.append(errorMessage);
        });
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", HttpStatus.BAD_REQUEST.value());
        response.put("error", "Validation Failed");
        response.put("message", message.toString());
        response.put("errors", errors);
        
        return ResponseEntity.badRequest().body(response);
    }
    
    /**
     * Handle bad credentials.
     */
    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<Map<String, Object>> handleBadCredentials(BadCredentialsException ex) {
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", HttpStatus.UNAUTHORIZED.value());
        response.put("error", "Unauthorized");
        response.put("message", "Invalid email or password");
        
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
    }
    
    /**
     * Handle access denied.
     */
    @ExceptionHandler(AccessDeniedException.class)
    public ResponseEntity<Map<String, Object>> handleAccessDenied(AccessDeniedException ex) {
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", HttpStatus.FORBIDDEN.value());
        response.put("error", "Forbidden");
        response.put("message", "Access denied");
        
        return ResponseEntity.status(HttpStatus.FORBIDDEN).body(response);
    }
    
    /**
     * Handle resource not found.
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<Map<String, Object>> handleResourceNotFound(ResourceNotFoundException ex) {
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", HttpStatus.NOT_FOUND.value());
        response.put("error", "Not Found");
        response.put("message", ex.getMessage());
        
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(response);
    }
    
    /**
     * Handle ML service exceptions.
     */
    @ExceptionHandler(MLServiceException.class)
    public ResponseEntity<Map<String, Object>> handleMLServiceException(MLServiceException ex) {
        log.error("ML Service error: {}", ex.getMessage());
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", HttpStatus.SERVICE_UNAVAILABLE.value());
        response.put("error", "ML Service Error");
        response.put("message", ex.getMessage());
        
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(response);
    }
    
    /**
     * Handle runtime exceptions.
     */
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, Object>> handleRuntimeException(RuntimeException ex) {
        log.error("Runtime error: {}", ex.getMessage());
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", HttpStatus.BAD_REQUEST.value());
        response.put("error", "Bad Request");
        response.put("message", ex.getMessage());
        
        return ResponseEntity.badRequest().body(response);
    }
    
    /**
     * Handle all other exceptions.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleException(Exception ex) {
        log.error("Unexpected error: {}", ex.getMessage(), ex);
        
        Map<String, Object> response = new HashMap<>();
        response.put("timestamp", LocalDateTime.now().toString());
        response.put("status", HttpStatus.INTERNAL_SERVER_ERROR.value());
        response.put("error", "Internal Server Error");
        response.put("message", "An unexpected error occurred");
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(response);
    }
}
