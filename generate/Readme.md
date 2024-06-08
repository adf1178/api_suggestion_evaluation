This project is to generate benchmarks for completing thrid-party APIs

## Data structure

Original file is `java_spring_api.json`

The followings are important keys of each item:

- project_name: The project name and corresponding version
- code: The function that contains the API (with comment)
- left_context: The code before `code`
- right_context: The code after `code`
- test_function: Test cases, may be empty
- import_text[List]: The import library of the file
- comment: The comment of the function that uses the API


## Generate benchmarks

### Fill the config.yaml

TYPE: `how/when/select`

whether use comment `USE_COMMENT: False`

whether use file context `USE_FILE_CONTEXT: False`

if use file context, how many lines before `LINE_BEFORE: 10`

whether use import message `USE_IMPORT_MESSAGE: True`

whether include library candidates: `USE_LIBRARY_CANDIDATE`

whether fill in the middle (use right context) `FILL_IN_THE_MIDDLE: False`

The filename of the saved benchmark file`SAVE_FILE_NAME: how_to_use_function_import`


### Run generate_benchmark.py


```
python generate_benchmark.py
```

# Examples

## Function Context (Base)
```java
@Override
	public VehicleDetails getVehicleDetails(VehicleIdentificationNumber vin)
			throws VehicleIdentificationNumberNotFoundException {
                // Expected
                Assert.notNull(vin, "VIN must not be null");

                // Right context
                logger.debug("Retrieving vehicle data for: " + vin);
                try {
                    return this.restTemplate.getForObject("/vehicle/{vin}/details", VehicleDetails.class, vin);
                }
                catch (HttpStatusCodeException ex) {
                    if (HttpStatus.NOT_FOUND.equals(ex.getStatusCode())) {
                        throw new VehicleIdentificationNumberNotFoundException(vin, ex);
                    }
                    throw ex;
                }
            }
```


## Function + Comment
```java
/**
 * Ensures that an object is not null. If it is, throws a customized IllegalArgumentException.
 *
 * @param object the object to check
 * @param message the exception message to use if the assertion fails
 * @throws IllegalArgumentException if the object is null
 */
/**
 * This method retrieves the vehicle details for a given VIN.
 * It first checks if the VIN is not null and logs the retrieval process.
 * Then it attempts to get the vehicle details from a RESTful web service.
 * If the VIN is not found in the web service, it throws a VehicleIdentificationNumberNotFoundException.
 * If any other HTTP status code is returned, it re-throws the HttpStatusCodeException.
 *
 * @param vin the Vehicle Identification Number
 * @return the vehicle details
 * @throws VehicleIdentificationNumberNotFoundException if the VIN is not found in the web service
 * @throws HttpStatusCodeException if any other HTTP status code is returned
 */

@Override
	public VehicleDetails getVehicleDetails(VehicleIdentificationNumber vin)
			throws VehicleIdentificationNumberNotFoundException {
                // Expected
                Assert.notNull(vin, "VIN must not be null");

                // Right context
                logger.debug("Retrieving vehicle data for: " + vin);
                try {
                    return this.restTemplate.getForObject("/vehicle/{vin}/details", VehicleDetails.class, vin);
                }
                catch (HttpStatusCodeException ex) {
                    if (HttpStatus.NOT_FOUND.equals(ex.getStatusCode())) {
                        throw new VehicleIdentificationNumberNotFoundException(vin, ex);
                    }
                    throw ex;
                }
            }
```

## Function + Import
```java
import org.apache.commons.logging.Log
import org.apache.commons.logging.LogFactory
import smoketest.test.domain.VehicleIdentificationNumber
import org.springframework.boot.web.client.RestTemplateBuilder
import org.springframework.http.HttpStatus
import org.springframework.stereotype.Service
import org.springframework.util.Assert
import org.springframework.web.client.HttpStatusCodeException
import org.springframework.web.client.RestTemplate
@Override
	public VehicleDetails getVehicleDetails(VehicleIdentificationNumber vin)
			throws VehicleIdentificationNumberNotFoundException {
                // Expected
                Assert.notNull(vin, "VIN must not be null");

                // Right context
                logger.debug("Retrieving vehicle data for: " + vin);
                try {
                    return this.restTemplate.getForObject("/vehicle/{vin}/details", VehicleDetails.class, vin);
                }
                catch (HttpStatusCodeException ex) {
                    if (HttpStatus.NOT_FOUND.equals(ex.getStatusCode())) {
                        throw new VehicleIdentificationNumberNotFoundException(vin, ex);
                    }
                    throw ex;
                }
            }
```

## File level (10 lines before the function)
```java
	private static final Log logger = LogFactory.getLog(RemoteVehicleDetailsService.class);

	private final RestTemplate restTemplate;

	public RemoteVehicleDetailsService(ServiceProperties properties, RestTemplateBuilder restTemplateBuilder) {
		this.restTemplate = restTemplateBuilder.rootUri(properties.getVehicleServiceRootUrl()).build();
	}


@Override
	public VehicleDetails getVehicleDetails(VehicleIdentificationNumber vin)
			throws VehicleIdentificationNumberNotFoundException {
                // Expected
                Assert.notNull(vin, "VIN must not be null");

                // Right context
                logger.debug("Retrieving vehicle data for: " + vin);
                try {
                    return this.restTemplate.getForObject("/vehicle/{vin}/details", VehicleDetails.class, vin);
                }
                catch (HttpStatusCodeException ex) {
                    if (HttpStatus.NOT_FOUND.equals(ex.getStatusCode())) {
                        throw new VehicleIdentificationNumberNotFoundException(vin, ex);
                    }
                    throw ex;
                }
            }
```