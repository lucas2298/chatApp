-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th10 26, 2019 lúc 02:46 AM
-- Phiên bản máy phục vụ: 10.4.8-MariaDB
-- Phiên bản PHP: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `chatbot`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `alltag`
--

CREATE TABLE `alltag` (
  `tag` varchar(32) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `locks` varchar(32) DEFAULT NULL,
  `question` varchar(255) DEFAULT NULL,
  `private` varchar(3) DEFAULT NULL,
  `response` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `alltag`
--

INSERT INTO `alltag` (`tag`, `description`, `locks`, `question`, `private`, `response`) VALUES
('advice', 'Tư vấn về tuyển dụng hoặc khách hàng', 'tuyendung', '', 'no', 'Bạn muốn tư vấn về phần nào?'),
('companyInformation', 'Thông tin công ty', 'advice_yes_no', 'Bạn muốn được tư vấn tiếp không?', 'no', 'Aureole Information Technology Inc.(AIT)-Công ty 100% vốn đầu tư cổ phần Mitani Sangyo. Phát triển phần mềm ứng dụng trên Web. <a style=\'color: black;\' target=\'_blank\' href=\'http://www.aureole.vn/ait/vietnamese/index.html\'>Chi tiết xem thêm tại đây.</a>'),
('employees', 'Liên quan đến nhân viên chính thức', '', '', 'no', 'Bạn hãy gửi CV về email: tuyendung@aureole-it.vn'),
('endConversation', 'Kết thúc trò chuyện', 'endConversation', 'Bạn muốn được tư vấn tiếp không?', 'no', 'Hẹn gặp lại.'),
('fresherInformation', 'Thông tin về chương trình fresher và internship', 'sendCV', 'Bạn có muốn nộp CV không?', 'yes', 'Chương trình fresher và internship được diễn ra hằng năm. Kết quả tuyển chọn dựa trên bài test và phỏng vấn.'),
('fresherInternship', 'Muốn biết gì về chương trình fresher và internship', 'fresherInformation', '', 'no', 'Bạn muốn biết gì về chương trình này?'),
('greeting', 'Chào hỏi', '', '', 'no', 'Mình có thể giúp gì cho bạn?'),
('noSendCV', 'Không gửi CV', 'noSendCV', '', 'yes', 'Bạn có cần gì nữa không?'),
('recruitmentInformation', 'Thông tin tuyển dụng', '', '', 'no', 'Các vị trí công ty có tuyển dụng'),
('sendCV', 'Có gửi CV', '', '', 'yes', 'Bạn hãy gửi CV về email: tuyendung@aureole-it.vn');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `keyunlock`
--

CREATE TABLE `keyunlock` (
  `id` int(11) NOT NULL,
  `tag` varchar(32) DEFAULT NULL,
  `keyUnlock` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `keyunlock`
--

INSERT INTO `keyunlock` (`id`, `tag`, `keyUnlock`) VALUES
(1, 'greeting', 'endConversation'),
(2, 'advice', 'advice_yes_no'),
(3, 'advice', 'noSendCV'),
(4, 'recruitmentInformation', 'tuyendung'),
(5, 'fresherInformation', 'fresherInformation'),
(6, 'noSendCV', 'sendCV'),
(7, 'sendCV', 'sendCV'),
(8, 'sendCV', 'fresherInformation'),
(9, 'endConversation', 'advice_yes_no'),
(10, 'endConversation', 'noSendCV');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `patterns`
--

CREATE TABLE `patterns` (
  `id` int(11) NOT NULL,
  `tag` varchar(32) DEFAULT NULL,
  `patterns` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `patterns`
--

INSERT INTO `patterns` (`id`, `tag`, `patterns`) VALUES
(1, 'greeting', 'hi'),
(2, 'greeting', 'hello'),
(3, 'greeting', 'chao'),
(4, 'greeting', 'chao ban'),
(5, 'greeting', 'bot'),
(6, 'greeting', 'can giup do'),
(7, 'greeting', 'xin chao'),
(8, 'greeting', 'ho tro'),
(9, 'companyInformation', 'thong tin cong ty'),
(10, 'companyInformation', 'thong tin'),
(11, 'companyInformation', 'thong tin co ban'),
(12, 'companyInformation', 'cong ty'),
(13, 'companyInformation', 'co ban'),
(14, 'advice', 'tu van'),
(15, 'advice', 'co'),
(16, 'recruitmentInformation', 'ung tuyen'),
(17, 'recruitmentInformation', 'thong tin tuyen dung'),
(18, 'recruitmentInformation', 'tuyen dung'),
(19, 'recruitmentInformation', 'tro thanh nhan vien'),
(20, 'recruitmentInformation', 'tro thanh'),
(21, 'fresherInternship', 'fresher'),
(22, 'fresherInternship', 'internship'),
(23, 'fresherInternship', 'fresher/internship'),
(24, 'fresherInternship', 'intern'),
(25, 'fresherInformation', 'thong tin'),
(26, 'noSendCV', 'khong cam on'),
(27, 'sendCV', 'co'),
(28, 'sendCV', 'nop cv nhu the nao'),
(29, 'employees', 'nhan vien chinh thuc'),
(30, 'employees', 'chinh thuc'),
(31, 'endConversation', 'ket thuc'),
(32, 'endConversation', 'tam biet'),
(33, 'endConversation', 'khong'),
(34, 'endConversation', 'khong cam on'),
(35, 'endConversation', 'im di'),
(36, 'endConversation', 'khong can'),
(37, 'endConversation', 'im lang');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `selectlist`
--

CREATE TABLE `selectlist` (
  `id` int(11) NOT NULL,
  `tag` varchar(32) DEFAULT NULL,
  `selects` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `selectlist`
--

INSERT INTO `selectlist` (`id`, `tag`, `selects`) VALUES
(1, 'greeting', 'Thông tin công ty.'),
(2, 'greeting', 'Tư vấn.'),
(3, 'companyInformation', 'Có'),
(4, 'companyInformation', 'Không, cảm ơn.'),
(5, 'advice', 'Tuyển dụng'),
(6, 'advice', 'Khách hàng'),
(7, 'recruitmentInformation', 'Fresher/Internship.'),
(8, 'recruitmentInformation', 'Nhân viên chính thức.'),
(9, 'fresherInternship', 'Thông tin'),
(10, 'fresherInternship', 'Nộp CV như thế nào?'),
(11, 'fresherInformation', 'Có'),
(12, 'fresherInformation', 'Không, cảm ơn'),
(13, 'noSendCV', 'Có'),
(14, 'noSendCV', 'Không, cảm ơn'),
(15, 'endConversation', 'Có.'),
(16, 'endConversation', 'Không, cảm ơn.');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `alltag`
--
ALTER TABLE `alltag`
  ADD PRIMARY KEY (`tag`);

--
-- Chỉ mục cho bảng `keyunlock`
--
ALTER TABLE `keyunlock`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tag` (`tag`);

--
-- Chỉ mục cho bảng `patterns`
--
ALTER TABLE `patterns`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tag` (`tag`);

--
-- Chỉ mục cho bảng `selectlist`
--
ALTER TABLE `selectlist`
  ADD PRIMARY KEY (`id`),
  ADD KEY `tag` (`tag`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `keyunlock`
--
ALTER TABLE `keyunlock`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT cho bảng `patterns`
--
ALTER TABLE `patterns`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT cho bảng `selectlist`
--
ALTER TABLE `selectlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `keyunlock`
--
ALTER TABLE `keyunlock`
  ADD CONSTRAINT `keyunlock_ibfk_1` FOREIGN KEY (`tag`) REFERENCES `alltag` (`tag`);

--
-- Các ràng buộc cho bảng `patterns`
--
ALTER TABLE `patterns`
  ADD CONSTRAINT `patterns_ibfk_1` FOREIGN KEY (`tag`) REFERENCES `alltag` (`tag`);

--
-- Các ràng buộc cho bảng `selectlist`
--
ALTER TABLE `selectlist`
  ADD CONSTRAINT `selectlist_ibfk_1` FOREIGN KEY (`tag`) REFERENCES `alltag` (`tag`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
