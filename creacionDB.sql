-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mibasededatos
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mibasededatos
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mibasededatos` DEFAULT CHARACTER SET utf8 ;
USE `mibasededatos` ;

-- -----------------------------------------------------
-- Table `mibasededatos`.`cuentas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mibasededatos`.`cuentas` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `saldo` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mibasededatos`.`transacciones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mibasededatos`.`transacciones` (
  `ID` INT NULL AUTO_INCREMENT,
  `IDCuena` VARCHAR(45) NOT NULL,
  `tipo` VARCHAR(45) NOT NULL,
  `monto` DECIMAL(10,2) NOT NULL,
  `fecha` DATE NOT NULL,
  `cuentas_ID` INT NOT NULL,
  PRIMARY KEY (`ID`, `cuentas_ID`),
  INDEX `fk_transacciones_cuentas_idx` (`cuentas_ID` ASC) VISIBLE,
  CONSTRAINT `fk_transacciones_cuentas`
    FOREIGN KEY (`cuentas_ID`)
    REFERENCES `mibasededatos`.`cuentas` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
