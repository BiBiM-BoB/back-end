import { Module } from '@nestjs/common';
import { SecurityResultService } from 'src/services/security_result.service';
import { SecurityResultController } from 'src/controllers/security_result/security_result.controller';

@Module({
  imports: [],
  controllers: [SecurityResultController],
  providers: [SecurityResultService],
})
export class SecurityResultModule {}