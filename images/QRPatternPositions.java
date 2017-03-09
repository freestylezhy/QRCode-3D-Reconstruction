package qr_detector;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import javax.imageio.ImageIO;

import com.google.zxing.BinaryBitmap;
import com.google.zxing.EncodeHintType;
import com.google.zxing.MultiFormatReader;
import com.google.zxing.NotFoundException;
import com.google.zxing.Result;
import com.google.zxing.ResultPoint;
import com.google.zxing.WriterException;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.qrcode.decoder.ErrorCorrectionLevel;

public class QRPatternPositions {

	public static void main(String[] args) throws WriterException, IOException, NotFoundException {

		// String charset = "UTF-8"; // or "ISO-8859-1"

		Map hintMap = new HashMap();
		hintMap.put(EncodeHintType.ERROR_CORRECTION, ErrorCorrectionLevel.L);

		String folder = ".";
		String filename;
		String filePath;

		int start = 6719;
		int end = 6727;
		
		for (int i = start; i <= end; i++) {
			filename = "IMG_" + i + ".JPG";
			filePath = folder + filename;

			BinaryBitmap binaryBitmap = new BinaryBitmap(
					new HybridBinarizer(new BufferedImageLuminanceSource(ImageIO.read(new FileInputStream(filePath)))));
			Result qrCodeResult = new MultiFormatReader().decode(binaryBitmap, hintMap);

			//System.out.println("Data read from QR Code: " + qrCodeResult.getText());
			
			int height = binaryBitmap.getHeight();
			
			ResultPoint points[] = qrCodeResult.getResultPoints();
			
			System.out.println(filename);
			for (ResultPoint point : points) {
				System.out.print(height-point.getY() + "\t" + point.getX() + "\t");
			}
			System.out.println();
		}
	}
}
