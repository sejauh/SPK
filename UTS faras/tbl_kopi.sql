-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 31, 2023 at 05:40 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `daftar_coffeeshop`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_kopi`
--

CREATE TABLE `tbl_kopi` (
  `nama_coffeeshop` varchar(20) NOT NULL,
  `kualitas_kopi` varchar(20) NOT NULL,
  `pelayanan` varchar(20) NOT NULL,
  `lokasi` varchar(20) NOT NULL,
  `harga` varchar(20) NOT NULL,
  `wifi` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tbl_kopi`
--

INSERT INTO `tbl_kopi` (`nama_coffeeshop`, `kualitas_kopi`, `pelayanan`, `lokasi`, `harga`, `wifi`) VALUES
('kopi_tuku', '1,096571589', '1,340884514', '1', '1', '1,340884514'),
('filosofi_kopi', '1,157329776', '1,447938172', '1', '0,831622098', '1,447938172'),
('lugs_coffee', '1', '1', '1,24573094', '1', '1,340884514'),
('bijeh_coffee', '1,096571589', '1', '1', '1', '1,203303026'),
('kopi_nako', '1', '1,203303026', '1,148698355', '0,911933166', '1,340884514'),
('kedua_coffee', '1,157329776', '1,340884514', '1', '0,864057955', '1,447938172'),
('leora_coffee', '1,096571589', '1,340884514', '1,148698355', '0,911933166', '1'),
('join_kopi', '1', '1,203303026', '1,148698355', '1', '1'),
('sejauh', '1,157329776', '1,447938172', '1,24573094', '0,864057955', '1,447938172'),
('the_pine', '1,096571589', '1,447938172', '1,24573094', '0,911933166', '1,340884514');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
