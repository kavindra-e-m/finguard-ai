package com.finguard.exception;

/**
 * Exception thrown when ML service call fails.
 */
public class MLServiceException extends RuntimeException {
    
    public MLServiceException(String message) {
        super(message);
    }
    
    public MLServiceException(String message, Throwable cause) {
        super(message, cause);
    }
}
