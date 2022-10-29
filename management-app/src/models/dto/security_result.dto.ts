import { IsJSON, IsNotEmpty, IsNumber, IsObject, IsString, MaxLength } from "class-validator";
export class CreateSecurityResultDto {

    @IsNotEmpty()
    readonly data: object;
}